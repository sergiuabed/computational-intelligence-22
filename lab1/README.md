# Lab 1: Set Covering

## Info for the Reader

Group members:

- Sergiu Abed (s295149)

- Luca Balduzzi (s303326)

- Riccardo Musumarra (s295103)

Main files on which the code has been developed: 

- lab01.py

## Task

Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$,
determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$
such that each number between $0$ and $N-1$ appears in at least one list

$$\forall n \in [0, N-1] \ \exists i : n \in L_{s_i}$$

and that the total numbers of elements in all $L_{s_i}$ is minimum.

## Approach

The search function utilized is based on the general graph search algorithm, provided by the professor in his slides, and it is set as breadth-first with some optimizations.

## State

A *State class* is used to store the necessary data. To explain its workings, let us consider an instance of it called *state*. It comprises a list of lists of integers called *state.solution* and a set of integers called *state.cover*. The object *state.solution* is the actual state the tree search is based on: we want its lists to have minimal instersections among each others. The object *state.cover* represents the unique integers covered by *state.solution*; it is used to check if a state has reached the goal state, that is full coverage of the integers from 0 to N-1, to compute one the cost measures and to optimize the space of possible actions.
Once *state.solution* has reached the goal state, the goodness of the result is evaluated using the *weight*, the sum of the lengths of *state.solution* lists and the *bloat*, the relative difference between *weight* and the length of *state.cover*.


## Actions

In this context, an "action" is the act of adding a list to the *state.solution*, forming a new state, and "discovering a node" means to add the new state to the frontier according to its computed priority.
Calculation the space of possible action is trivial, since it is only the set difference between the lists in *state.solution* and the collection of all lists.
Given that the size of the frontier become quickly unmanageable with $N > 30$, it is necessary to decrease the number of discovered nodes. To achieve this, we only select actions that actually increase the cover. 
Unfortunately this is not effective enough, thus we performed a statistical discrimination based on the bloat. More precisely, we computed the bloat of all of the new states that resulted from adding each of the remaining lists from the previous step. Then we compute the average of such collection, and discarded all the actions the resulted in a greater than average bloat. This last selection, similar to a beam search, was quite effective in reducing memory utilization, even though deprives us the guarantee of completeness given by the breadth-first search.


## Node Cost

The cost of an action is computed as the sum of two terms:

- a measure of impurity (repeated integers), the resuting size of the intersection between *state.cover* and the cover of the action, divided by the length of the action;

- a measure of simplicity (choosing longer lists to reach the goal state faster): the length of the action over N.

## Priority Function

The priority function is simply the cost of the *new_state*.

## Results

- N = 5, W = 5, Bloat: 0%, Visited Nodes = 3

- N = 10, W = 10, Bloat: 0%, Visited Nodes = 3

- N = 20, W = 23, Bloat: 15%, Visited Nodes = 449

- N = 50, W = 66, Bloat: 32%, Visited Nodes = 61898

- N = 100: not tried, given the increase of visited nodes for smaller N.

### Sources

- Giovanni Squillero's Github Computational Intelligence

- 8 Puzzle Solution

- Giovanni Squillero's Slides of the course Computational Intelligence 2022/2023
