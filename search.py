import math
import heapq
import time

from dataclasses import dataclass, field
from typing import List

import resource
from resource import RUSAGE_SELF


class PuzzleState():
    """ complete information about particular tiles configuration

    Arguments
    ----------
    tiles_config : list[int]
        initial position of tiles
    parent : PuzzleState, optional
        PuzzleState which led to the current, by default None
    direction : str, optional
        direction of the move which led from the parent to current state,
        by default ''
    zero_index : int, optional
        index of the empty tile, default None
    ast : bool, optional
        True if A* method is used
        (additional attributes should be initialized), by default False

    Attributes
    ----------
        state : list[int]
            tiles configuration
        string_state : str
            tiles configuration as string
        parent: PuzzleState, optional
            PuzzleState which led to the current, by default None
        direction : str, optional
            direction of the move which led from the parent to current state
        ast : bool, optional
            True if A* method is used
            (additional attributes should be initialized), by default False
        depth : int
            depth of the current element in the search tree
        zero_index : int
            index of the zero element

    """
    def __init__(self, tiles_config, parent=None, direction='',
                 zero_index=None, ast=False,
                 coords2d=None, score=None):
        self.state = tiles_config
        self.string_state = ",".join(map(str, self.state))
        self.parent = parent
        self.direction = direction
        self.ast = ast
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        if zero_index:
            self.zero_index = zero_index
        else:
            self.zero_index = self.state.index(0)
        if ast:
            if coords2d:
                self.coords2d = coords2d
            else:
                self.coords2d = coords_2d(self.state)
            if score:
                self.score = score
            else:
                self.score = self.manhatten_distance_to_goal()\
                    + self.depth

    def __repr__(self):
        """ for pretty printing

        Returns
        -------
        str
            configuration with line breaks to print a tiles in 2d format
        """
        global side
        return "\n".join(
            [" ".join(map(str, self.state[i*side:(i+1)*side]))
             for i in range(side)]
                        ) + "\n"

    def __lt__(self, other):
        """comparison between two PuzzleState instances"""
        return self.score < other.score

    def manhatten_distance_to_goal(self):
        dist = 0.0
        global coords_goal
        for key in range(1, len(self.state)):
            dist += abs(coords_goal[key][0] - self.coords2d[key][0]) +\
                abs(coords_goal[key][1] - self.coords2d[key][1])
        return dist

    def neighbours(self):
        """generator of possible movement directions in order \"UDLR\"

        Yields
        -------
        str
            direction where it is possible to move zero element
        """
        global side
        if self.zero_index >= side and self.direction != "D":
            yield "U"
        if self.zero_index < len(self.state) - side and self.direction != "U":
            yield "D"
        if self.zero_index % side != 0 and self.direction != "R":
            yield "L"
        if self.zero_index % side != side - 1 and self.direction != "L":
            yield "R"

    def neighbours_rev(self):
        """the same as neightbours(), but in reversed order"""
        global side
        if self.zero_index % side != side - 1 and self.direction != "L":
            yield "R"
        if self.zero_index % side != 0 and self.direction != "R":
            yield "L"
        if self.zero_index < len(self.state) - side and self.direction != "U":
            yield "D"
        if self.zero_index >= side and self.direction != "D":
            yield "U"

    def make_move(self, direction):
        """change a configuration with moving a zero element in the desired direction

        Parameters
        ----------
        direction : str, {"U", "D", "L", "R"}

        Returns
        -------
        PuzzleState
            an instance of PuzzleState obtained after moving performed
        """
        new_state = list(self.state)
        global side
        if direction == "U":
            new_state[self.zero_index], new_state[self.zero_index-side] =\
                new_state[self.zero_index-side], new_state[self.zero_index]
            zero_index_delta = -side
        elif direction == "D":
            new_state[self.zero_index], new_state[self.zero_index+side] =\
                new_state[self.zero_index+side], new_state[self.zero_index]
            zero_index_delta = side
        elif direction == "L":
            new_state[self.zero_index], new_state[self.zero_index-1] =\
                new_state[self.zero_index-1], new_state[self.zero_index]
            zero_index_delta = -1
        elif direction == "R":
            new_state[self.zero_index], new_state[self.zero_index+1] =\
                new_state[self.zero_index+1], new_state[self.zero_index]
            zero_index_delta = 1
        return PuzzleState(new_state, parent=self, direction=direction,
                           zero_index=self.zero_index + zero_index_delta)

    def make_move_ast(self, direction):
        """change a configuration with moving a zero element in the desired direction

        Parameters
        ----------
        direction : str, {"U", "D", "L", "R"}

        Returns
        -------
        PuzzleState
            an instance of PuzzleState obtained after moving performed
        """
        new_state = list(self.state)
        coords2d = self.coords2d.copy()
        global side, coords_goal
        if direction == "U":
            new_state[self.zero_index], new_state[self.zero_index-side] =\
                new_state[self.zero_index-side], new_state[self.zero_index]
            coords2d[0] = (coords2d[0][0] - 1, coords2d[0][1])
            coords2d[new_state[self.zero_index]] =\
                (coords2d[new_state[self.zero_index]][0] + 1,
                 coords2d[new_state[self.zero_index]][1])
            manh_diff = abs(coords_goal[new_state[self.zero_index]][0] -
                            coords2d[new_state[self.zero_index]][0])\
                - abs(coords_goal[new_state[self.zero_index]][0] -
                      self.coords2d[new_state[self.zero_index]][0])
            zero_index_delta = -side
        elif direction == "D":
            new_state[self.zero_index], new_state[self.zero_index+side] =\
                new_state[self.zero_index+side], new_state[self.zero_index]
            coords2d[0] = (coords2d[0][0] + 1, coords2d[0][1])
            coords2d[new_state[self.zero_index]] =\
                (coords2d[new_state[self.zero_index]][0] - 1,
                 coords2d[new_state[self.zero_index]][1])
            manh_diff = abs(coords_goal[new_state[self.zero_index]][0] -
                            coords2d[new_state[self.zero_index]][0])\
                - abs(coords_goal[new_state[self.zero_index]][0] -
                      self.coords2d[new_state[self.zero_index]][0])
            zero_index_delta = side
        elif direction == "L":
            new_state[self.zero_index], new_state[self.zero_index-1] =\
                new_state[self.zero_index-1], new_state[self.zero_index]
            coords2d[0] = (coords2d[0][0], coords2d[0][1] - 1)
            coords2d[new_state[self.zero_index]] =\
                (coords2d[new_state[self.zero_index]][0],
                 coords2d[new_state[self.zero_index]][1] + 1)
            manh_diff = abs(coords_goal[new_state[self.zero_index]][1] -
                            coords2d[new_state[self.zero_index]][1])\
                - abs(coords_goal[new_state[self.zero_index]][1] -
                      self.coords2d[new_state[self.zero_index]][1])
            zero_index_delta = -1
        elif direction == "R":
            new_state[self.zero_index], new_state[self.zero_index+1] =\
                new_state[self.zero_index+1], new_state[self.zero_index]
            coords2d[0] = (coords2d[0][0], coords2d[0][1] + 1)
            coords2d[new_state[self.zero_index]] =\
                (coords2d[new_state[self.zero_index]][0],
                 coords2d[new_state[self.zero_index]][1] - 1)
            manh_diff = abs(coords_goal[new_state[self.zero_index]][1] -
                            coords2d[new_state[self.zero_index]][1])\
                - abs(coords_goal[new_state[self.zero_index]][1] -
                      self.coords2d[new_state[self.zero_index]][1])
            zero_index_delta = 1
        return PuzzleState(new_state, parent=self, direction=direction,
                           zero_index=self.zero_index + zero_index_delta,
                           ast=self.ast,
                           coords2d=coords2d, score=self.score+manh_diff+1)


class Solver():
    """A class which solves an 8 puzzle game

    Returns
    -------
    PuzzleState or None
        A final state if the search was successfull or None if not

    Args
    ----------
    method : str, {"bfs", "dfs", "ast"}
        a method to solve a game
    array : list[int]
        initial position of tiles
    zl : bool
        True if zero is a last element of the goal array,
        default False

    Attributes
    ----------
        _method : str
            method of solving
        goal_array : list
            goal tiles configuration
        goal : str
            goal tiles configuration in a format of string
        initial_state : PuzzleState
            initial state
        statistics : Stats
            holds all the neccessary statistics data
        final_state : PuzzleState
            final element

    Raises
    ------
    AttributeError
        if the parity of initial state and the goal are not the same, that
        is a system is not solvable
    """
    # TODO make a function to compare all methods

    def __init__(self, method, array, zl=False):
        global side, coords_goal
        side = int(math.sqrt(len(array)))
        self._method = method
        if zl:
            self.goal_array = list(range(1, len(array))) + [0]
        else:
            self.goal_array = list(range(len(array)))
        coords_goal = coords_2d(self.goal_array)
        self.initial_state = PuzzleState(list(array), ast=(method == "ast"))
        self.goal = ",".join(map(str, self.goal_array))
        self.statistics = Stats()
        self.final_state = None
        if not self.check_solvability():
            raise AttributeError("The initial state is not solvable")

    def is_goal(self, state):
        return state.string_state == self.goal

    def solve(self, maxnodes=500000):
        if self._method == "bfs":
            self.final_state = self.bfs(maxnodes=maxnodes)
        elif self._method == "dfs":
            self.final_state = self.dfs(maxnodes=maxnodes)
        elif self._method == "ast":
            self.final_state = self.ast(maxnodes=maxnodes)
        if self.final_state:
            self.get_path()
        self.statistics.end_time = time.time()
        self.statistics.total_time = self.statistics.end_time -\
            self.statistics.start_time
        return self.final_state

    def bfs(self, maxnodes):
        queue = [self.initial_state]
        queue_strs = {self.initial_state.string_state}
        visited = {''}
        while queue:
            current_state = queue.pop(0)
            queue_strs.remove(current_state.string_state)

            if self.is_goal(current_state):
                return current_state
            self.statistics.nodes += 1
            if self.statistics.nodes > maxnodes:
                break
            visited.add(current_state.string_state)

            for d in current_state.neighbours():
                new_s = current_state.make_move(d)
                if (new_s.string_state not in visited) and\
                        (new_s.string_state not in queue_strs):
                    queue.append(new_s)
                    queue_strs.add(new_s.string_state)
                    if new_s.depth > self.statistics.max_depth:
                        self.statistics.max_depth = new_s.depth

    def dfs(self, maxnodes):
        queue = [self.initial_state]
        queue_strs = {self.initial_state.string_state}
        visited = {''}
        while queue:
            current_state = queue.pop()
            queue_strs.remove(current_state.string_state)
            if current_state.depth > self.statistics.max_depth:
                self.statistics.max_depth = current_state.depth

            if self.is_goal(current_state):
                return current_state
            self.statistics.nodes += 1
            if self.statistics.nodes > maxnodes:
                break
            visited.add(current_state.string_state)

            for d in current_state.neighbours_rev():
                new_s = current_state.make_move(d)
                if (new_s.string_state not in visited) and\
                        (new_s.string_state not in queue_strs):
                    queue.append(new_s)
                    queue_strs.add(new_s.string_state)

    def ast(self, maxnodes):
        queue = {self.initial_state.string_state: self.initial_state}
        hqueue = []
        heapq.heappush(hqueue, (self.initial_state.score,
                                self.initial_state.string_state))
        visited = {''}
        while hqueue:
            _, str = heapq.heappop(hqueue)
            current_state = queue[str]
            if current_state.depth > self.statistics.max_depth:
                self.statistics.max_depth = current_state.depth

            if self.is_goal(current_state):
                return current_state
            self.statistics.nodes += 1
            if self.statistics.nodes > maxnodes:
                break
            visited.add(current_state.string_state)

            for d in current_state.neighbours():
                new_s = current_state.make_move_ast(d)
                if new_s.string_state not in visited:
                    if new_s.string_state not in queue\
                     or queue[new_s.string_state].depth > new_s.depth:
                        heapq.heappush(hqueue,
                                       (new_s.score, new_s.string_state))
                        queue[new_s.string_state] = new_s

    def get_path(self):
        """add the full path of final element to the statistics object"""
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
        """print the statistics of the search process and (optionally) final path

        Arguments
        ---------
        print_path : bool
            whether to print a final path

        """
        if print_path:
            print("path_to_goal: ", self.statistics.moves)
        print("cost_of_path: ", len(self.statistics.moves))
        print("nodes_expanded: ", self.statistics.nodes)
        if self.final_state:
            print("search_depth: ", self.final_state.depth)
        print("max_depth: ", self.statistics.max_depth)
        print("running_time: ",
              round(time.time() - self.statistics.start_time, 3), "s")
        print("max_ram_usage: {} MB"
              .format(resource.getrusage(RUSAGE_SELF)[2]/1000))

    def check_solvability(self):
        global side
        return parity(self.initial_state.state) ==\
               parity(self.goal_array) * (-1)**(side + 1)


@dataclass
class Stats():
    nodes: int = 0
    max_depth: int = 0
    path: List[PuzzleState] = field(default_factory=list)
    moves: List[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    total_time: float = 0.0


def coords_2d(arr):
    """transform an array to the 2d coordinates

        Returns
        -------
        dict
            keys are an initial array and values -
            a tuples of x and y coordinates
    """
    # side = int(math.sqrt(len(arr)))
    global side
    return {num: (i//side, i % side) for i, num in enumerate(arr)}


def parity(nums):
    nums = [num for num in nums if num != 0]
    sor = nums.copy()
    sor.sort()
    par = 1
    while nums != sor:
        for i in range(len(nums)-1):
            if nums[i] > nums[i+1]:
                nums[i], nums[i+1] = nums[i+1], nums[i]
                par *= -1
    return par
