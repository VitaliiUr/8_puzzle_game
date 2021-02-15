# 8_puzzle_game

The program solves the 8-puzzle game using different search methods: Deep search first, Breadth search first and A*.

The game is to take a $n \times n$ board with $n^2-1$ tiles in a range from 1 to ($n^2-1$) and moving 
empty space come to the position when all the tiles are sorted by they values.

So the goal is to obtain:

```
*,1,2
3,4,5
6,7,8
```
for $n=3$. * represent an empty space


For example the game can be:

3,1,2    3,1,2    3,1,2    *,1,2
4,7,5    4,*,5    *,4,5    3,4,5
6,*,8    6,7,8    6,7,8    6,7,8

So the final result is a set of movements ("U","D","L","R") which lead from the initial position to the goal.


### Usage

```
python3 puzzle_8.py <method> <initial_position> [--f] [--n]
```

Method can be 'dfs'(deep search first), 'bfs'(breadth search first) or 'ast'(A*).

Initial position is a comma-separated set of numbers, which represent an initial position on the bord. An empty space is 
substituted by number 0.

Flag --f defines whether the set of movements should be displayed at the end(default False).

Flag --n defines a maximum number of nodes (positions) to visit during the search process.



### Note

Not all the initial positions can lead to the goal. The condition is that the parity of the
initial position and goal are the same as each movement does not change a parity.
This condition is checked before the start of searching.
