#!/usr/bin/env python3
import argparse
import math


class PuzzleState():
    def __init__(self, init_state, parent=None, direction='', zero=None):
        self.state = init_state
        self.strs = "".join(map(str, self.state))
        self.parent = parent
        self.direction = direction
        self.dist = self.manhatten_distance_to_goal()
        if parent:
            self.side = parent.side
            self.depth = parent.depth + 1
        else:
            self.depth = 0
            self.side = int(math.sqrt(len(init_state)))
        if zero:
            self.zero = zero
        else:
            self.zero = self.state.index(0)

    def __repr__(self):
        return "\n".join(
            [" ".join(map(str, self.state[i*self.side:(i+1)*self.side]))
             for i in range(self.side)]
                        ) + "\n"

    def __lt__(self, other):
        # return (self.dist, "UDLR".find(self.direction)) <\
            #    (other.dist, "UDLR".find(other.direction))
        return (self.dist, self.depth, "UDLR".find(self.direction)) <\
               (other.dist, other.depth, "UDLR".find(other.direction))
        # return self.dist < other.dist

    def manhatten_distance_to_goal(self):
        dist = 0.0
        coords = coords_2d(self.state)
        coords_g = coords_2d(range(len(self.state)))
        for key in range(1, len(self.state)):
            dist += abs(coords_g[key][0] - coords[key][0]) +\
                abs(coords_g[key][1] - coords[key][1])
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
                               zero=self.zero-self.side)
        elif direction == "D":
            new_state[self.zero], new_state[self.zero+self.side] =\
                new_state[self.zero+self.side], new_state[self.zero]
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero+self.side)
        elif direction == "L":
            new_state[self.zero], new_state[self.zero-1] =\
                new_state[self.zero-1], new_state[self.zero]
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero-1)
        elif direction == "R":
            new_state[self.zero], new_state[self.zero+1] =\
                new_state[self.zero+1], new_state[self.zero]
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero+1)


def coords_2d(arr):
    side = int(math.sqrt(len(arr)))
    return {num: (i//side, i % side) for i, num in enumerate(arr)}


class Solver():

    def __init__(self, method, array):
        self._method = method
        self.goal = "".join(map(str, sorted(list(array))))
        self.initial_state = PuzzleState(list(array))
        self.true_2d = coords_2d(sorted(array))

    def is_goal(self, state):
        return state.strs == self.goal

    def solve(self, verbose=False, maxnodes=500000):
        if self._method == "bfs":
            final_state = self.bfs(verbose=verbose,
                                   maxnodes=maxnodes)
        elif self._method == "dfs":
            final_state = self.dfs(verbose=verbose,
                                   maxnodes=maxnodes)
        elif self._method == "ast":
            final_state = self.ast(verbose=verbose,
                                   maxnodes=maxnodes)
        return final_state

    def bfs(self, verbose=False, maxnodes=200000):
        queue = [self.initial_state]
        visited = {''}
        nodes = 0
        max_depth = 0
        while queue:
            current_state = queue.pop(0)
            if current_state.depth > max_depth:
                max_depth = current_state.depth

            if self.is_goal(current_state):
                print(f"{nodes} nodes")
                print(f"{current_state.depth} depth")
                print(f"{max_depth} max depth")
                return current_state
            nodes += 1

            for d in current_state.neighbours():
                new_s = current_state.make_move(d)
                if new_s.strs not in visited:
                    queue.append(new_s)
                    visited.add(new_s.strs)

            if nodes > maxnodes:
                print(f"{nodes} nodes")
                print(f"{current_state.depth} depth")
                print(f"{max_depth} max depth")
                break

    def dfs(self, verbose=False, maxnodes=200000):
        queue = [self.initial_state]
        visited = {''}
        nodes = 0
        max_depth = 0
        while queue:
            current_state = queue.pop()
            if current_state.depth > max_depth:
                max_depth = current_state.depth

            if self.is_goal(current_state):
                print(f"{nodes} nodes")
                print(f"{current_state.depth} depth")
                print(f"{max_depth} max depth")
                return current_state
            nodes += 1

            for d in current_state.neighbours_rev():
                new_s = current_state.make_move(d)
                if new_s.strs not in visited:
                    queue.append(new_s)
                    visited.add(new_s.strs)

            if nodes > maxnodes:
                print(f"{nodes} nodes")
                print(f"{current_state.depth} depth")
                print(f"{max_depth} max depth")
                break

    def ast(self, verbose=False, maxnodes=200000):
        queue = [self.initial_state]
        visited = {''}
        nodes = 0
        max_depth = 0
        while queue:
            queue = sorted(queue, reverse=True)
            current_state = queue.pop()
            if verbose:
                print("Winner ", current_state.direction)
                print(current_state.dist)
                print(current_state)
                for state in queue:
                    print(state.state)
                    print(state.dist)
                # print(len(queue))
            if current_state.depth > max_depth:
                max_depth = current_state.depth

            if self.is_goal(current_state):
                print(f"{nodes} nodes")
                print(f"{current_state.depth} depth")
                print(f"{max_depth} max depth")
                return current_state
            nodes += 1
            visited.add(current_state.strs)

            if verbose:
                print("neightbours")
            for d in current_state.neighbours():
                new_s = current_state.make_move(d)
                if verbose:
                    print("---> ", d, " --->")
                    print(new_s.dist)
                    print(new_s)
                # print("--->  --->")
                # print(next((x for x in queue if x.strs == new_s.strs), [""]).depth)
                if new_s.strs not in visited:
                    queue.append(new_s)
                # else:

            if nodes > maxnodes:
                print(f"{nodes} nodes")
                print(f"{current_state.depth} depth")
                print(f"{max_depth} max depth")
                break


def print_path(state):
    path = [state]
    moves = [state.direction]
    par = state.parent
    while par:
        path.append(par)
        moves.append(par.direction)
        par = par.parent
    # for el in path[::-1]:
    #     print(el)
    print(moves[-2::-1])
    print("Cost of path: ", len(moves[-2::-1]))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("method", default="bfs",
                        help="method of search: bfs, dfs or ast")
    parser.add_argument("initial", default="0,1,2,3,4,5,6,7,8",
                        help="initial state of puzzle in format: 0,1,2,3 etc")
    parser.add_argument("-f", "--final", action='store_true',
                        help="initial state of puzzle in format: 0,1,2,3 etc")
    parser.add_argument("-d", "--debug", action='store_true',
                        help="initial state of puzzle in format: 0,1,2,3 etc")
    args = parser.parse_args()

    init_state = list(map(int, args.initial.split(",")))
    if (list(range(len(init_state))) != sorted(init_state)):
        raise ValueError("Wrong initial state! Check if all numbers are here")
    if (math.sqrt(len(init_state)) != round(math.sqrt(len(init_state)))):
        raise ValueError("Wrong initial state! Check the side size")
    solver = Solver(args.method, init_state)
    final_state = solver.solve(verbose=args.debug, maxnodes=200000)
    if args.final:
        if final_state:
            print_path(final_state)
        else:
            print("Solution is not found")
