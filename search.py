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
    zero : int, optional
        index of the empty tile, by default None
    ast : bool, optional
        True if A* method is used
        (additional attributes should be initialized), by default False

    Attributes
    ----------
        state : list[int]
            tiles configuration
        strs : str
            tiles configuration as string
        parent: PuzzleState, optional
            PuzzleState which led to the current, by default None
        direction : str, optional
            direction of the move which led from the parent to current state
        ast : bool, optional
            True if A* method is used
            (additional attributes should be initialized), by default False
        side : int
            size of 2d space of tiles
        depth : int
            depth of the current element in the search tree
        coords_goal : dict
            2d coordinates of the goal configuration
        zero : int
            index of the zero element

    """
    def __init__(self, tiles_config, parent=None, direction='',
                 zero=None, ast=False, goal_array=None,
                 coords2d=None, dist=None):
        self.state = tiles_config
        self.strs = "".join(map(str, self.state))
        self.parent = parent
        self.direction = direction
        self.ast = ast
        if parent:
            self.side = parent.side
            self.depth = parent.depth + 1
        else:
            self.depth = 0
            self.side = int(math.sqrt(len(tiles_config)))
        if zero:
            self.zero = zero
        else:
            self.zero = self.state.index(0)
        if ast:
            if parent:
                self.coords_goal = parent.coords_goal
            else:
                self.coords_goal = coords_2d(goal_array, self.side)
            if coords2d:
                self.coords2d = coords2d
            else:
                self.coords2d = coords_2d(self.state, self.side)

            # OR
            if dist:
                self.dist = dist
            else:
                self.dist = self.manhatten_distance_to_goal(self.coords_goal)\
                    + self.depth
            # self.dist = self.manhatten_distance_to_goal(self.coords_goal) +\
            #     self.depth

    def __repr__(self):
        """ for pretty printing

        Returns
        -------
        str
            configuration with line breaks to print a tiles in 2d format
        """
        return "\n".join(
            [" ".join(map(str, self.state[i*self.side:(i+1)*self.side]))
             for i in range(self.side)]
                        ) + "\n"

    def __lt__(self, other):
        """comparison between two PuzzleState instances"""
        # return (self.dist, "UDLR".find(self.direction)) <\
        # (other.dist, "UDLR".find(other.direction))
        return self.dist < other.dist

    def manhatten_distance_to_goal(self, coords_goal):
        dist = 0.0
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
        if self.zero >= self.side and self.direction != "D":
            yield "U"
        if self.zero < len(self.state) - self.side and self.direction != "U":
            yield "D"
        if self.zero % self.side != 0 and self.direction != "R":
            yield "L"
        if self.zero % self.side != 2 and self.direction != "L":
            yield "R"

    def neighbours_rev(self):
        """the same as neightbours(), but in reversed order"""
        if self.zero % self.side != 2 and self.direction != "L":
            yield "R"
        if self.zero % self.side != 0 and self.direction != "R":
            yield "L"
        if self.zero < len(self.state) - self.side and self.direction != "U":
            yield "D"
        if self.zero >= self.side and self.direction != "D":
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
        coords2d = self.coords2d.copy()
        if direction == "U":
            new_state[self.zero], new_state[self.zero-self.side] =\
                new_state[self.zero-self.side], new_state[self.zero]
            coords2d[0] = (coords2d[0][0] - 1, coords2d[0][1])
            coords2d[new_state[self.zero]] =\
                (coords2d[new_state[self.zero]][0] + 1,
                 coords2d[new_state[self.zero]][1])
            manh_diff = abs(self.coords_goal[new_state[self.zero]][0] -
                            coords2d[new_state[self.zero]][0])\
                - abs(self.coords_goal[new_state[self.zero]][0] -
                      self.coords2d[new_state[self.zero]][0])
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero-self.side, ast=self.ast,
                               coords2d=coords2d, dist=self.dist+manh_diff+1)
        elif direction == "D":
            new_state[self.zero], new_state[self.zero+self.side] =\
                new_state[self.zero+self.side], new_state[self.zero]
            coords2d[0] = (coords2d[0][0] + 1, coords2d[0][1])
            coords2d[new_state[self.zero]] =\
                (coords2d[new_state[self.zero]][0] - 1,
                 coords2d[new_state[self.zero]][1])
            manh_diff = abs(self.coords_goal[new_state[self.zero]][0] -
                            coords2d[new_state[self.zero]][0])\
                - abs(self.coords_goal[new_state[self.zero]][0] -
                      self.coords2d[new_state[self.zero]][0])
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero+self.side, ast=self.ast,
                               coords2d=coords2d, dist=self.dist+manh_diff+1)
        elif direction == "L":
            new_state[self.zero], new_state[self.zero-1] =\
                new_state[self.zero-1], new_state[self.zero]
            coords2d[0] = (coords2d[0][0], coords2d[0][1] - 1)
            coords2d[new_state[self.zero]] =\
                (coords2d[new_state[self.zero]][0],
                 coords2d[new_state[self.zero]][1] + 1)
            manh_diff = abs(self.coords_goal[new_state[self.zero]][1] -
                            coords2d[new_state[self.zero]][1])\
                - abs(self.coords_goal[new_state[self.zero]][1] -
                      self.coords2d[new_state[self.zero]][1])
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero-1, ast=self.ast,
                               coords2d=coords2d, dist=self.dist+manh_diff+1)
        elif direction == "R":
            new_state[self.zero], new_state[self.zero+1] =\
                new_state[self.zero+1], new_state[self.zero]
            coords2d[0] = (coords2d[0][0], coords2d[0][1] + 1)
            coords2d[new_state[self.zero]] =\
                (coords2d[new_state[self.zero]][0],
                 coords2d[new_state[self.zero]][1] - 1)
            manh_diff = abs(self.coords_goal[new_state[self.zero]][1] -
                            coords2d[new_state[self.zero]][1])\
                - abs(self.coords_goal[new_state[self.zero]][1] -
                      self.coords2d[new_state[self.zero]][1])
            return PuzzleState(new_state, parent=self, direction=direction,
                               zero=self.zero+1, ast=self.ast,
                               coords2d=coords2d, dist=self.dist+manh_diff+1)

    # def get_goal_config(self):
    #     return sorted(list(self.state))


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

    def __init__(self, method, array, goal_array=None):
        self._method = method
        if goal_array:
            self.goal_array = goal_array
        else:
            self.goal_array = list(range(len(array)))
        self.initial_state = PuzzleState(list(array), ast=(method == "ast"),
                                         goal_array=self.goal_array)
        self.goal = "".join(map(str, self.goal_array))
        self.statistics = Stats()
        self.final_state = None
        if not self.check_solvability():
            raise AttributeError("The initial state is not solvable")

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
            # print(current_state)
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
        queue = []
        heapq.heappush(queue, (self.initial_state, self.initial_state.depth))
        queue_strs = {self.initial_state.strs}
        visited = {''}
        while queue:
            state = heapq.heappop(queue)
            # print(state[0].strs)
            current_state = state[0]
            # queue_strs.remove(current_state.strs)
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
                # if new_s.strs not in visited:
                    # if new_s.strs not in queue_strs:
                heapq.heappush(queue, (new_s, new_s.depth))
                queue_strs.add(new_s.strs)
                    # TODO sorted dictionary
                    # else:
                    #     for i, el in enumerate(queue):
                    #         if el[0].strs == new_s.strs:
                    #             elem, num = el[0], i
                    #             break
                    #     if new_s.depth < elem.depth:
                    #         queue[num] = (new_s, new_s.depth)

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
        print("running_time: ", time.time() - self.statistics.start_time)
        print("max_ram_usage: {} MB"
              .format(resource.getrusage(RUSAGE_SELF)[2]/1000))

    def check_solvability(self):
        # return True
        # print(parity(self.initial_state.state))
        return parity(self.initial_state.state) ==\
               parity(self.goal_array) * (-1)**(self.initial_state.side + 1)


@dataclass
class Stats():
    nodes: int = 0
    max_depth: int = 0
    path: List[PuzzleState] = field(default_factory=list)
    moves: List[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)


def coords_2d(arr, side):
    """transform an array to the 2d coordinates

        Returns
        -------
        dict
            keys are an initial array and values -
            a tuples of x and y coordinates
    """
    # side = int(math.sqrt(len(arr)))
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
