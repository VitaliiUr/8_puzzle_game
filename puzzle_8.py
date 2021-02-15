#!/usr/bin/env python3
import argparse
import math
from search import Solver


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
                        help="maximum number of nodes to visit,\
                             default 200 000")
    args = parser.parse_args()

    init_state = list(map(int, args.initial.split(",")))
    if (list(range(len(init_state))) != sorted(init_state)):
        raise ValueError("Wrong initial state! Check if all numbers are here")
    if (math.sqrt(len(init_state)) != round(math.sqrt(len(init_state)))):
        raise ValueError("Wrong initial state! Check the array size")
    solver = Solver(args.method, init_state)
    final_state = solver.solve(maxnodes=int(args.nodes))
    solver.print_stats(args.final)
    if not final_state:
        print("Solution is not found")
