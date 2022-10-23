import unittest
from familytree.familygraph import FamilyGraph
import os


class TestFamilyGraph(unittest.TestCase):
    def setUp(self):
        self.fg = FamilyGraph()
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../family_dataset.txt')
        self.fg.populate_graph(filename)

    def test_add_child(self):
        """
        1. If you try to add to not available node, print error
        2. If you added the child successfully, print message
        3. If you try to add to male, print error
        :return:
        """
        self.assertEqual(self.fg.add_child('Lisa', 'Te', 'M'), "PERSON_NOT_FOUND")
        self.assertEqual(self.fg.add_child('Flora', 'Minerva', 'F'), "CHILD_ADDED")
        self.assertEqual(self.fg.add_child('Bill', 'Zoe', 'F'), "CHILD_ADDITION_FAILED")

    def test_get_relationship(self):
        # 1. If you try to get non-exiting relationship, return None
        # 2. Check if correct relationships are returned
        self.assertEqual(self.fg.get_relationship('Charlie', 'Spouse'), [])
        self.assertEqual(self.fg.get_relationship('Rose', 'Spouse'), ['Malfoy'])
        self.assertEqual(self.fg.get_relationship('Queen-Margret', 'Son'), ['Bill', 'Charlie', 'Percy', 'Ronald'])
        self.assertEqual(self.fg.get_relationship('King-Arthur', 'Daughter'), ['Ginerva'])
        self.assertEqual(self.fg.get_relationship('Harry', 'Brother-In-Law'), ['Bill', 'Charlie', 'Percy', 'Ronald'])
        self.assertEqual(self.fg.get_relationship('James', 'Brother-In-Law'), [])
        self.assertEqual(self.fg.get_relationship('James', 'Sister-In-Law'), ['Alice'])
        self.assertEqual(self.fg.get_relationship('James', 'Maternal-Uncle'), ['Bill', 'Charlie', 'Percy', 'Ronald'])
        self.assertEqual(self.fg.get_relationship('Draco', 'Paternal-Uncle'), [])
        self.assertEqual(self.fg.get_relationship('Remus', 'Maternal-Uncle'), ['Louis'])
        self.assertEqual(self.fg.get_relationship('Remus', 'Maternal-Aunt'), ['Dominique'])

        # Add a child and see if the correct relationships are returned
        self.fg.add_child('Flora', 'Minerva', 'F')
        self.assertEqual(self.fg.get_relationship('Minerva', 'Paternal-Uncle'), ['Charlie', 'Percy', 'Ronald'])
        self.assertEqual(self.fg.get_relationship('Remus', 'Maternal-Aunt'), ['Dominique', 'Minerva'])
        self.assertEqual(self.fg.get_relationship('Remus', 'Paternal-Aunt'), [])
        self.assertEqual(self.fg.get_relationship('Ted', 'Sister-In-Law'), ['Dominique', 'Minerva'])
        self.assertEqual(self.fg.get_relationship('Minerva', 'Nephew'), ['Remus'])

        self.fg.add_child('Ginerva', 'Kasun', 'M')
        self.assertEqual(self.fg.get_relationship('Kasun', 'Father'), ['Harry'])
        self.assertEqual(self.fg.get_relationship('Kasun', 'Maternal-Uncle'), ['Bill', 'Charlie', 'Percy', 'Ronald'])
        self.assertEqual(self.fg.get_relationship('Kasun', 'Niece'), ['Ginny'])
        self.assertEqual(self.fg.get_relationship('Ron', 'Paternal-Uncle'), ['James', 'Kasun'])
        self.assertEqual(self.fg.get_relationship('Darcy', 'Brother-In-Law'), ['Albus', 'Kasun'])

    # def tearDown(self):
    #     self.fg.dispose()
