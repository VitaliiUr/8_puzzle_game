#!/usr/bin/env python3
import argparse
import math


class PuzzleState():
    def __init__(self, init_state, parent=None, direction='',
                 zero=None, ast=None):
        self.state = init_state
        self.strs = "".join(map(str, self.state))
        self.parent = parent
        self.direction = direction
        self.ast = ast
        if parent:
            self.side = parent.side
            self.depth = parent.depth + 1
            self.coords_goal = parent.coords_goal
        else:
            self.depth = 0
            self.side = int(math.sqrt(len(init_state)))
            self.coords_goal = coords_2d(range(len(self.state)))
        if zero:
            self.zero = zero
        else:
            self.zero = self.state.index(0)
        if ast:
            if parent:
                self.coords_goal = parent.coords_goal
            else:
                self.coords_goal = coords_2d(range(len(self.state)))
            self.dist = self.manhatten_distance_to_goal(self.coords_goal) +\
                        self.depth

    def __repr__(self):
        return "\n".join(
            [" ".join(map(str, self.state[i*self.side:(i+1)*self.side]))
             for i in range(self.side)]
                        ) + "\n"

    def __lt__(self, other):
        # return (self.dist, "UDLR".find(self.direction)) < (other.dist, "UDLR".find(other.direction))
        return self.dist < other.dist

    def manhatten_distance_to_goal(self, coords_goal):
        dist = 0.0
        coords = coords_2d(self.state)
        for key in range(1, len(self.state)):
            dist += abs(coords_goal[key][0] - coords[key][0]) +\
                abs(coords_goal[key][1] - coords[key][1])
        return dist

    def neighbours(self,):
        if self.zero >= self.side and self.direction != "D":
            yield "U"
        if self.zero < len(self.state) - self.side and self.direction != "U":
            yield "D"
        if self.zero % self.side != 0 and self.direction != "R":
            yield "L"
        if self.zero % self.side != 2 and self.direction != "L":
            yield "R"

    def neighbours_rev(self):
        if self.zero % self.side != 2 and self.direction != "L":
            yield "R"
        if self.zero % self.side != 0 and self.direction != "R":
            yield "L"
        if self.zero < len(self.state) - self.side and self.direction != "U":
            yield "D"
        if self.zero >= self.side and self.direction != "D":
            yield "U"

    def make_move(self, direction):
        new_state = list(self.state)
        if direction == "U":
            new_state[self.zero], new_state[self.zero-self.side] =\
                new_state[self.zero-self.side], new_state[self.zero]
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero-self.side, ast=self.ast)
        elif direction == "D":
            new_state[self.zero], new_state[self.zero+self.side] =\
                new_state[self.zero+self.side], new_state[self.zero]
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero+self.side, ast=self.ast)
        elif direction == "L":
            new_state[self.zero], new_state[self.zero-1] =\
                new_state[self.zero-1], new_state[self.zero]
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero-1, ast=self.ast)
        elif direction == "R":
            new_state[self.zero], new_state[self.zero+1] =\
                new_state[self.zero+1], new_state[self.zero]
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero+1, ast=self.ast)


def coords_2d(arr):
    side = int(math.sqrt(len(arr)))
    return {num: (i//side, i % side) for i, num in enumerate(arr)}


class Solver():

    def __init__(self, method, array):
        self._method = method
        self.goal = "".join(map(str, sorted(list(array))))
        self.initial_state = PuzzleState(list(array), ast=(method == "ast"))
        self.true_2d = coords_2d(sorted(array))
        self.statistics = Stats()
        self.final_state = None

    def is_goal(self, state):
        return state.strs == self.goal

    def solve(self, maxnodes=500000):
        if self._method == "bfs":
            self.final_state = self.bfs(maxnodes=maxnodes)
        elif self._method == "dfs":
            self.final_state = self.dfs(maxnodes=maxnodes)
        elif self._method == "ast":
            self.final_state = self.ast(maxnodes=maxnodes)
        if self.final_state:
            self.get_path()
        return self.final_state

    def bfs(self, maxnodes=200000):
        queue = [self.initial_state]
        queue_strs = {self.initial_state.strs}
        visited = {''}
        while queue:
            current_state = queue.pop(0)
            queue_strs.remove(current_state.strs)
            if current_state.depth > self.statistics.max_depth:
                self.statistics.max_depth = current_state.depth

            if self.is_goal(current_state):
                return current_state
            self.statistics.nodes += 1
            if self.statistics.nodes > maxnodes:
                break
            visited.add(current_state.strs)

            for d in current_state.neighbours():
                new_s = current_state.make_move(d)
                if (new_s.strs not in visited) and\
                        (new_s.strs not in queue_strs):
                    queue.append(new_s)
                    queue_strs.add(new_s.strs)

    def dfs(self, maxnodes=200000):
        queue = [self.initial_state]
        queue_strs = {self.initial_state.strs}
        visited = {''}
        while queue:
            current_state = queue.pop()
            queue_strs.remove(current_state.strs)
            if current_state.depth > self.statistics.max_depth:
                self.statistics.max_depth = current_state.depth

            if self.is_goal(current_state):
                return current_state
            self.statistics.nodes += 1
            if self.statistics.nodes > maxnodes:
                break
            visited.add(current_state.strs)

            for d in current_state.neighbours_rev():
                new_s = current_state.make_move(d)
                if (new_s.strs not in visited) and\
                        (new_s.strs not in queue_strs):
                    queue.append(new_s)
                    queue_strs.add(new_s.strs)

    def ast(self, maxnodes=200000):
        queue = [self.initial_state]
        queue_strs = {self.initial_state.strs}
        visited = {''}
        while queue:
            queue = sorted(queue, reverse=True)
            current_state = queue.pop()
            queue_strs.remove(current_state.strs)
            if current_state.depth > self.statistics.max_depth:
                self.statistics.max_depth = current_state.depth

            if self.is_goal(current_state):
                return current_state
            self.statistics.nodes += 1
            if self.statistics.nodes > maxnodes:
                break
            visited.add(current_state.strs)

            for d in current_state.neighbours():
                new_s = current_state.make_move(d)
                if new_s.strs not in visited:
                    if new_s.strs not in queue_strs:
                        queue.append(new_s)
                        queue_strs.add(new_s.strs)
                    else:
                        elem, num = [(el, i) for i, el in enumerate(queue) if el.strs == new_s.strs][0]
                        if new_s.depth < elem.depth:
                            queue[num] = new_s

    def get_path(self):
        self.statistics.path = [self.final_state]
        moves = [self.final_state.direction]
        par = self.final_state.parent
        while par:
            self.statistics.path.append(par)
            moves.append(par.direction)
            par = par.parent
        self.statistics.path = self.statistics.path[::-1]
        self.statistics.moves = moves[-2::-1]

    def print_stats(self, print_path):
        if print_path:
            print("path_to_goal: ", self.statistics.moves)
        print("cost_of_path: ", len(self.statistics.moves))
        print("nodes_expanded: ", self.statistics.nodes)
        print("search_depth: ", self.final_state.depth)
        print("max_depth: ", self.statistics.max_depth)


class Stats():
    def __init__(self):
        self.nodes = 0
        self.max_depth = 0
        self.path = []
        self.moves = []


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("method", default="bfs",
                        help="method of search: bfs, dfs or ast")
    parser.add_argument("initial", default="0,1,2,3,4,5,6,7,8",
                        help="initial state of puzzle in format: 0,1,2,3 etc,\
                        default 0,1,2,3,4,5,6,7,8")
    parser.add_argument("-f", "--final", action='store_true',
                        help="print the path")
    parser.add_argument("-n", "--nodes", default='200000',
                        help="maximum number of nodes to visit, default 200000")
    args = parser.parse_args()

    init_state = list(map(int, args.initial.split(",")))
    if (list(range(len(init_state))) != sorted(init_state)):
        raise ValueError("Wrong initial state! Check if all numbers are here")
    if (math.sqrt(len(init_state)) != round(math.sqrt(len(init_state)))):
        raise ValueError("Wrong initial state! Check the side size")
    solver = Solver(args.method, init_state)
    final_state = solver.solve(maxnodes=int(args.nodes))
    if final_state:
        solver.print_stats(args.final)
    else:
        print("Solution is not found")
