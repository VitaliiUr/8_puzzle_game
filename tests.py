import unittest
from search import Solver


class TestPuzzle(unittest.TestCase):

    puzzle_3_1 = [8,6,4,2,1,3,5,7,0]
    puzzle_3_2 = [6,1,8,4,0,2,7,3,5]
    puzzle_4_zl = [1,2,3,4,13,9,14,5,12,10,15,0,11,8,7,6]

    def test_ast1(self):
        solver = Solver("ast", self.puzzle_3_1)
        _ = solver.solve()
        print(round(solver.statistics.total_time, 3), " s")
        self.assertEqual(solver.statistics.max_depth, 26)
        self.assertEqual(solver.statistics.moves, ['L', 'U', 'U', 'L', 'D', 'R', 'D', 'L', 'U', 'R', 'R', 'U', 'L', 'L', 'D', 'R', 'R', 'U', 'L', 'D', 'D', 'R', 'U', 'L', 'U', 'L'])

    def test_ast2(self):
        solver = Solver("ast", self.puzzle_3_2)
        _ = solver.solve()
        print(round(solver.statistics.total_time, 3), " s")
        self.assertEqual(solver.statistics.max_depth, 20)
        self.assertEqual(solver.statistics.moves, ['D', 'R', 'U', 'U', 'L', 'D', 'R', 'D', 'L', 'U', 'L', 'U', 'R', 'R', 'D', 'D', 'L', 'L', 'U', 'U'])

    def test_bfs1(self):
        solver = Solver("bfs", self.puzzle_3_1)
        _ = solver.solve()
        print(round(solver.statistics.total_time, 3), " s")
        self.assertEqual(solver.statistics.max_depth, 27)
        self.assertEqual(solver.statistics.nodes, 166786)
        self.assertEqual(solver.statistics.moves, ['L', 'U', 'U', 'L', 'D', 'R', 'D', 'L', 'U', 'R', 'R', 'U', 'L', 'L', 'D', 'R', 'R', 'U', 'L', 'D', 'D', 'R', 'U', 'L', 'U', 'L'])

    def test_bfs2(self):
        solver = Solver("bfs", self.puzzle_3_2)
        _ = solver.solve()
        print(round(solver.statistics.total_time, 3), " s")
        self.assertEqual(solver.statistics.max_depth, 21)
        self.assertEqual(solver.statistics.nodes, 54094)
        self.assertEqual(solver.statistics.moves, ['D', 'R', 'U', 'U', 'L', 'D', 'R', 'D', 'L', 'U', 'L', 'U', 'R', 'R', 'D', 'D', 'L', 'L', 'U', 'U'])

    def test_dfs1(self):
        solver = Solver("dfs", self.puzzle_3_1)
        _ = solver.solve()
        print(round(solver.statistics.total_time, 3), " s")
        self.assertEqual(solver.statistics.max_depth, 9612)
        self.assertEqual(solver.statistics.nodes, 9869)

    def test_dfs2(self):
        solver = Solver("dfs", self.puzzle_3_2)
        _ = solver.solve()
        print(round(solver.statistics.total_time, 3), " s")
        self.assertEqual(solver.statistics.max_depth, 46142)
        self.assertEqual(solver.statistics.nodes, 51015)

    def test_ast3(self):
        solver = Solver("ast", self.puzzle_4_zl, zl=True)
        _ = solver.solve()
        print(round(solver.statistics.total_time, 3), " s")
        self.assertEqual(solver.statistics.max_depth, 35)
        self.assertEqual(solver.statistics.moves, ['D', 'L', 'L', 'L', 'U', 'U', 'R', 'R', 'R', 'D', 'D', 'L', 'L', 'L', 'U', 'R', 'R', 'D', 'L', 'U', 'U', 'R', 'R', 'D', 'D', 'L', 'L', 'U', 'L', 'U', 'R', 'R', 'R', 'D', 'D']
)


if __name__ == '__main__':
    unittest.main()
