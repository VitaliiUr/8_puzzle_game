#!/usr/bin/env python3
import argparse
import math
import numpy as np


class PuzzleState():
    def __init__(self, init_state, parent=None, direction=''):
        self.state = init_state
        self.parent = parent
        self.direction = direction
        if parent:
            self.side = parent.side
            self.depth = parent.depth + 1
        else:
            self.depth = 0
            self.side = int(math.sqrt(len(init_state)))
        self.neighb = self.neighbours()

    def __repr__(self):
        return "\n".join(
            [" ".join(map(str, self.state[i*self.side:(i+1)*self.side]))
             for i in range(self.side)]
                        ) + "\n"

    def neighbours(self):
        res = []
        if self.state.index(0) >= self.side and self.direction != "D":
            res.append("U")
        if self.state.index(0) < self.side**2 - self.side and self.direction != "U":
            res.append("D")
        if self.state.index(0) % self.side != 0 and self.direction != "R":
            res.append("L")
        if self.state.index(0) % self.side != 2 and self.direction != "L":
            res.append("R")
        return res

    def make_move(self, direction):
        new_state = self.state.copy()
        z_ind = new_state.index(0)
        if direction == "U":
            new_state[z_ind], new_state[z_ind-self.side] =\
                new_state[z_ind-self.side], new_state[z_ind]
        elif direction == "D":
            new_state[z_ind], new_state[z_ind+self.side] =\
                new_state[z_ind+self.side], new_state[z_ind]
        elif direction == "L":
            new_state[z_ind], new_state[z_ind-1] =\
                new_state[z_ind-1], new_state[z_ind]
        elif direction == "R":
            new_state[z_ind], new_state[z_ind+1] =\
                new_state[z_ind+1], new_state[z_ind]
        if new_state != self.state:
            return PuzzleState(new_state, parent=self, direction=direction)
        else:
            return None

    def is_goal(self):
        return self.state == sorted(self.state)


def bfs(initial_state, verbose=False):
    queue = [initial_state]
    visited = []
    nodes = 0
    current_state = None
    max_depth = 0
    while queue:
        current_state = queue.pop(0)
        if current_state.depth > max_depth:
            max_depth = current_state.depth

        if current_state.is_goal():
            print(f"{nodes} nodes")
            print(f"{current_state.depth} depth")
            print(f"{max_depth} max depth")
            return current_state
        nodes += 1

        if verbose:
            print(current_state, current_state.neighb)
        for d in current_state.neighb:
            new_s = current_state.make_move(d)
            if verbose:
                print("--->", d, "--->")
                print(new_s)
            if new_s and new_s.state not in visited:
                queue.append(new_s)
                visited.append(new_s.state)

        if nodes > 10000:
            print(f"{nodes} nodes")
            print(f"{current_state.depth} depth")
            print(f"{max_depth} max depth")
            break


def dfs(initial_state, verbose=False):
    queue = [initial_state]
    visited = []
    nodes = 0
    max_depth = 0
    while queue:
        current_state = queue.pop()
        if current_state.depth > max_depth:
            max_depth = current_state.depth

        if current_state.is_goal():
            print(f"{nodes} nodes")
            print(f"{current_state.depth} depth")
            print(f"{max_depth} max depth")
            return current_state
        nodes += 1
        # else:
            # visited.append(current_state.state)

        if verbose:
            print(current_state, current_state.neighb[::-1])
        for d in current_state.neighb[::-1]:
            new_s = current_state.make_move(d)
            if new_s and new_s.state not in visited:
                if verbose:
                    print("--->", d, "--->")
                    print(new_s)
                queue.append(new_s)
                visited.append(new_s.state)

        # if nodes % 10000 == 0:
        #     print(nodes)
        if nodes > 100000:
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
    initial = PuzzleState(list(init_state))
    if args.method == "bfs":
        final_state = bfs(initial, args.debug)
    elif args.method == "dfs":
        final_state = dfs(initial, args.debug)
    if args.final:
        if final_state:
            print_path(final_state)
        else:
            print("Solution is not found")
