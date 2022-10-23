import networkx as nx
import csv


class FamilyGraph:
    """
    This class can be used to hold data related to family trees.
    """
    def __init__(self):
        self.fam_graph = nx.DiGraph()

    def populate_graph(self, file_path):
        # print("file_path " + file_path)
        # read from the text file. Text file is treated as a csv file.
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            headings = next(reader) # skip the header

            # data = list(reader)
            for item in list(reader):
                name, spouse_name, spouse_gender, child_name, child_gender = item
                if not self.fam_graph.has_node(name):
                    # Add mother. Gender is always female
                    self.fam_graph.add_node(name, gender='F')

                self.__add_spouse(name=name, spouse_name=spouse_name, spouse_gender=spouse_gender)
                self.add_child(mum_name=name, child_name=child_name, gender=child_gender)

        print("graph populated " + str(self.fam_graph.nodes))
        return True

    def get_relationship(self, name, relationship):
        relatives = []
        for nbr, datadict in self.fam_graph.adj[name].items():
            if nbr == name:
                continue
            if datadict['relationship'] == relationship:
                relatives.append(nbr)

        return relatives

    def __add_spouse(self, name, spouse_name, spouse_gender):
        # When you add a spouse to a node, it create in-laws
        # Add spouse, get siblings, add in-laws
        spouse = self.get_relationship(name, 'Spouse')
        if not spouse:
            # check if spouse node exists
            if self.fam_graph.has_node(spouse_name):
                self.fam_graph.add_edge(name, spouse_name, relationship='Spouse')
                self.fam_graph.add_edge(spouse_name, name, relationship='Spouse')
            else:
                self.fam_graph.add_node(spouse_name, gender=spouse_gender)
                self.fam_graph.add_edge(name, spouse_name, relationship='Spouse')
                self.fam_graph.add_edge(spouse_name, name, relationship='Spouse')

            # Now spouse is created. Let's create in-laws of the spouse's side
            # First get spouse's siblings
            s_siblings = self.get_relationship(spouse_name, 'Siblings')
            for sib in s_siblings:
                if self.fam_graph.nodes[sib]['gender'] == 'M':
                    # add brother-in-law & vice-versa
                    self.fam_graph.add_edge(name, sib, relationship='Brother-In-Law')
                    self.fam_graph.add_edge(sib, name, relationship='Sister-In-Law')
                else:
                    # add sister-in-law
                    self.fam_graph.add_edge(name, sib, relationship='Sister-In-Law')
                    self.fam_graph.add_edge(sib, name, relationship='Sister-In-Law')

            # Now create in-laws of mother's side for mother's spouse
            m_siblings = self.get_relationship(name, 'Siblings')
            for msib in m_siblings:
                if self.fam_graph.nodes[msib]['gender'] == 'M':
                    # add brother-in-law & vice-versa
                    self.fam_graph.add_edge(spouse_name, msib, relationship='Brother-In-Law')
                    # we assume that spouses keep husband-wife relationship even they are in a same sex relationship
                    self.fam_graph.add_edge(msib, spouse_name, relationship='Brother-In-Law')
                else:
                    # add brother-in-law & vice-versa
                    self.fam_graph.add_edge(spouse_name, msib, relationship='Sister-In-Law')
                    # we assume that spouses keep husband-wife relationship even they are in a same sex relationship
                    self.fam_graph.add_edge(msib, spouse_name, relationship='Brother-In-Law')

    def add_child(self, mum_name, child_name, gender):
        # print("adding " + mum_name + child_name + gender)
        if not self.fam_graph.has_node(mum_name):
            return "PERSON_NOT_FOUND"
        else:
            # now mum exists. Check if mum is female
            if self.fam_graph.nodes[mum_name]['gender'] == 'M':
                return "CHILD_ADDITION_FAILED"

            self.fam_graph.add_node(child_name, gender=gender)

            # now add relationships
            rship = 'Son' if gender == 'M' else 'Daughter'
            self.fam_graph.add_edge(mum_name, child_name, relationship=rship)
            self.fam_graph.add_edge(child_name, mum_name, relationship='Mother')

            dad = self.get_relationship(mum_name, 'Spouse')
            if dad:
                self.fam_graph.add_edge(dad[0], child_name, relationship=rship)
                self.fam_graph.add_edge(child_name, dad[0], relationship='Father')
                self.__add_paternal_side(dad_name=dad[0], child_name=child_name)

            self.__add_siblings(mum_name=mum_name, child_name=child_name)
            self.__add_maternal_side(mum_name=mum_name, child_name=child_name)

            # Add in-laws
            self.__add_in_laws(child_name, gender)
            # Add child's nieces and nephews
            self.__add_neice_nephew(child_name, gender)

            return "CHILD_ADDED"


    def __add_siblings(self, mum_name, child_name):
        # get mum's other children. No need to get dad's other children because we only add children via mum
        brothers = self.get_relationship(mum_name, 'Son')
        for bro in brothers:
            self.fam_graph.add_edge(child_name, bro, relationship='Siblings')
            self.fam_graph.add_edge(bro, child_name, relationship='Siblings')

        sisters = self.get_relationship(mum_name, 'Daughter')
        for sis in sisters:
            self.fam_graph.add_edge(child_name, sis, relationship='Siblings')
            self.fam_graph.add_edge(sis, child_name, relationship='Siblings')

    def __add_paternal_side(self, dad_name, child_name):
        # get dad's siblings
        siblings = self.get_relationship(dad_name, 'Siblings')
        for sib in siblings:
            if self.fam_graph.nodes[sib]['gender'] == 'M':
                # add uncle
                self.fam_graph.add_edge(child_name, sib, relationship='Paternal-Uncle')
            else:
                # add aunt
                self.fam_graph.add_edge(child_name, sib, relationship='Paternal-Aunt')

    def __add_maternal_side(self, mum_name, child_name):
        # get mum's siblings
        siblings = self.get_relationship(mum_name, 'Siblings')
        for sib in siblings:
            if self.fam_graph.nodes[sib]['gender'] == 'M':
                # add uncle
                self.fam_graph.add_edge(child_name, sib, relationship='Maternal-Uncle')
            else:
                # add aunt
                self.fam_graph.add_edge(child_name, sib, relationship='Maternal-Aunt')

    def __add_neice_nephew(self, person_name, person_gender):
        uncle_or_aunt = 'Aunt' if person_gender is 'F' else 'Uncle'
        siblings = self.get_relationship(person_name, 'Siblings')
        for sib in siblings:
            # check if sibling has any children
            for nbr, datadict in self.fam_graph.adj[sib].items():
                if nbr == sib:
                    continue
                if (datadict['relationship'] == 'Son') or (datadict['relationship'] == 'Daughter'):
                    if self.fam_graph.nodes[sib]['gender'] == 'M':
                        self.fam_graph.add_edge(nbr, person_name, relationship='Paternal-' + uncle_or_aunt)
                        if self.fam_graph.nodes[nbr]['gender'] == 'M':
                            self.fam_graph.add_edge(person_name, nbr, relationship='Nephew')
                        else:
                            self.fam_graph.add_edge(person_name, nbr, relationship='Niece')
                    else:
                        self.fam_graph.add_edge(nbr, person_name, relationship='Maternal-' + uncle_or_aunt)
                        if self.fam_graph.nodes[nbr]['gender'] == 'M':
                            self.fam_graph.add_edge(person_name, nbr, relationship='Nephew')
                        else:
                            self.fam_graph.add_edge(person_name, nbr, relationship='Niece')

    def __add_in_laws(self, person_name, person_gender):
        bro_or_sis = 'Brother' if person_gender is 'M' else 'Sister'
        siblings = self.get_relationship(person_name, 'Siblings')
        for sib in siblings:
            # check if sibling has a spouse
            for nbr, datadict in self.fam_graph.adj[sib].items():
                if nbr == sib:
                    continue
                if datadict['relationship'] == 'Spouse':
                    if self.fam_graph.nodes[nbr]['gender'] == 'M':
                        self.fam_graph.add_edge(person_name, nbr, relationship='Brother-In-Law')
                        self.fam_graph.add_edge(nbr, person_name, relationship=bro_or_sis + '-In-Law')
                    else:
                        self.fam_graph.add_edge(person_name, nbr, relationship='Sister-In-Law')
                        self.fam_graph.add_edge(nbr, person_name, relationship=bro_or_sis + '-In-Law')
