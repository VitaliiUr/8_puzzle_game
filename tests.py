import unittest
from search import Solver


class TestPuzzle(unittest.TestCase):

    puzzle_3_1 = [8,6,4,2,1,3,5,7,0]
    puzzle_3_2 = [6,1,8,4,0,2,7,3,5]


    def test_ast1(self):
        solver = Solver("ast", self.puzzle_3_1)
        final_state = solver.solve()
        # print(final_state)
        # print(solver.statistics.moves)
        self.assertEqual(solver.statistics.moves, ['L', 'U', 'U', 'L', 'D', 'R', 'D', 'L', 'U', 'R', 'R', 'U', 'L', 'L', 'D', 'R', 'R', 'U', 'L', 'D', 'D', 'R', 'U', 'L', 'U', 'L'])
    
    def test_ast2(self):
        solver = Solver("ast", self.puzzle_3_2)
        final_state = solver.solve()
        # print(final_state)
        # print(solver.statistics.moves)
        self.assertEqual(solver.statistics.moves, ['D', 'R', 'U', 'U', 'L', 'D', 'R', 'D', 'L', 'U', 'L', 'U', 'R', 'R', 'D', 'D', 'L', 'L', 'U', 'U'])

    # def test_isuper(self):
    #     self.assertTrue('FOO'.isuper())
    #     self.assertFalse('Foo'.isuper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()