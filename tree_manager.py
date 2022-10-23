import argparse
from cmd import Cmd
from familytree import familygraph as fg


class TreeManager(Cmd):

    prompt = ">> "
    fam_graph = fg.FamilyGraph()

    def populate_graph(self, datafile):
        print("populating the graph from {}".format(datafile))
        self.fam_graph.populate_graph(datafile)

    def do_ADD_CHILD(self, args):
        """
        Add a child to the family tree through mother.
        :param args: Mother's-Name Child's-Name Gender
        :return: status message
        """
        arg_list = args.rsplit(" ")
        if len(arg_list) != 3:
            print("{} arguments given. Three arguments are required".format(len(arg_list)))
            return
        try:
            msg = self.fam_graph.add_child(*arg_list)
            print(msg)
        except ValueError as e:
            print(e)

    def do_GET_RELATIONSHIP(self, args):
        """
        Get relationship data.
        :param args: Name Relationship
        :return: Related people
        """
        arg_list = args.rsplit(" ")
        if len(arg_list) != 2:
            print("{} arguments given. Two arguments are required".format(len(arg_list)))
            return
        try:
            msg = self.fam_graph.get_relationship(*arg_list)
            print(*msg) if msg else print('NONE')
        except KeyError:
            print("No relationships available")

    def do_exit(self, args):
        raise SystemExit()

if __name__ == '__main__':
    app = TreeManager()
    # generate the graph from a text file
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", help="Path to the data file")
    args = parser.parse_args()
    app.populate_graph(args.datafile)

    app.cmdloop('Enter a command to do something. eg `ADD_CHILD Mother\'s-Name Child\'s-Name Gender`')







