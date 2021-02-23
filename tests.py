import unittest
from search import Solver


class TestPuzzle(unittest.TestCase):

    def test_ast(self):
        solver = Solver("ast", [8,6,4,2,1,3,5,7,0])
        final_state = solver.solve()
        print(final_state)
        print(solver.statistics.moves)
        # self.assertEqual(solver.statistics.moves, ['L', 'U', 'U', 'L', 'D', 'R', 'D', 'L', 'U', 'R', 'R', 'U', 'L', 'L', 'D', 'R', 'R', 'U', 'L', 'D', 'D', 'R', 'U', 'L', 'U', 'L'])

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()