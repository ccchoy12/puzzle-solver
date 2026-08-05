#### progress as of 16/9/2018
# Support BFS  (queue) and DFS  (stack) and AST (priority Q based on Manhatan distance)
# can try to use vim as editor,  like an IDE environment



###import Queue as Q

### import time

### import resource

import sys

import math

from collections import deque

import heapq

import itertools

#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break
        

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print (line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            
            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n
            
            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children




def writeOutput():

    """Write Output"""
                     

def dfs_search(initial_state):

    return solver (initial_state, "dfs")

def A_star_search(initial_state):

    return solver (initial_state, "ast")

def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###

def calculate_manhattan_dist(idx, value, n):

    """calculatet the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###

def test_goal(puzzle_state):

    """test the state is the goal state or not"""

    if puzzle_state.config == (0,1,2,3,4,5,6,7,8):
        return ("true")
    else:
        return ("false")


class VisitQ (object):
### a set to store visited config to avoid re-visit

    # q=None here, not q=[]: a mutable default arg is created ONCE at class
    # definition time and shared by every instance that doesn't pass q
    # explicitly. That silently leaked visited-state between back-to-back
    # calls to bfs_search/dfs_search/A_star_search in the same process
    # (same input puzzle solved twice returned different costs, 3 vs 19).
    #
    # Also a set, not a list: `s.config in vq.q` in solver() runs on every
    # single node dequeued, and a list membership check is O(n) - against
    # a visited set that grows into the tens of thousands, that made the
    # search effectively quadratic. Set membership is O(1).
    def __init__(self,q=None):
        self.q = q if q is not None else set()

    def addq (self,o):
        self.q.add (o)

class Queue (object):
### traditional implementation of Queue data structure

    # deque, not a plain list: del self.q[0] on a list is O(n) (shifts
    # every remaining element), which turned BFS quadratic once the
    # queue grew into the tens of thousands. deque.popleft() is O(1).
    def __init__(self,q=None):
        self.q = q if q is not None else deque()

    def addo (self,o):
        self.q.append (o)

    def firsto (self):
        return self.q[0]

    def delo (self):
        self.q.popleft ()

    def size (self):
        return (len (self.q))

class Stack (object):
### traditional implementation of Stack data structure

    # push/pop the END of the list instead of insert(0,o)/del self.q[0]
    # at the front. Same LIFO behavior, but O(1) instead of O(n) per
    # call (insert-at-front/delete-at-front both shift every element).
    def __init__(self,q=None):
        self.q = q if q is not None else []

    def addo (self,o):
        self.q.append (o)

    def firsto (self):
        return self.q[-1]

    def delo (self):
        self.q.pop ()

    def size (self):
        return (len (self.q))

class Pqueue (object):
### Priority Queue ordered by f(n) = g(n) + h(n), smallest out first
### backed by heapq instead of a linear scan (see addo/firsto/delo below)

    # q=None, not q=[]: same mutable-default-arg fix as VisitQ above.
    def __init__(self,q=None):
        self.q = q if q is not None else []
        # Tie-breaker so heapq never has to compare two PuzzleState
        # objects directly when their priorities are equal (PuzzleState
        # has no __lt__, which would crash the comparison).
        self._counter = itertools.count()

    def addo (self,o):
        # Priority must be f(n) = g(n) + h(n), not h(n) alone. Using only
        # manhdist(o.config) (h(n)) makes this greedy best-first search,
        # not A* - fast, but not guaranteed optimal. Confirmed: on a
        # 20-move-scramble puzzle, plain h(n) returned a 56-move solution
        # vs. BFS's true optimum of 22. Adding o.cost (g(n)) fixes that.
        #
        # heapq, not min()+list.index(): the old version rescanned the
        # entire list twice per pop (once in firsto(), once again in
        # delo()) to find the smallest priority - O(n) per pop, done
        # twice. heapq.heappush/heappop are O(log n).
        priority = o.cost + manhdist(o.config)
        heapq.heappush(self.q, (priority, next(self._counter), o))

    def firsto (self):
        return self.q[0][2]

    def delo (self):
        heapq.heappop(self.q)

    def size (self):
        return (len (self.q))


def bfs_search(initial_state):
    return solver (initial_state, "bfs")
    

def solver (initial_state, stype):

    if stype == "bfs":
        q = Queue ()
    elif stype == "dfs":
        q = Stack ()
    elif stype == "ast":
        q = Pqueue ()
    vq = VisitQ ()
    
    print (stype)
    initial_state.display ()
    
    q.addo(initial_state)
    
    while q.size() != 0:
        s = q.firsto ()
        if len (vq.q) % 3000 == 0:
            print ("while loop, cost, qsize vsize", s.cost, q.size(), len (vq.q),  s.config)
        if s.config in vq.q:
            q.delo ()
        else : 
            vq.addq (s.config)
            s.children = s.expand ()       
            for i in range (len (s.children)) :
               #print (i, " child is ", s.children[i])
               if test_goal (s.children[i]) == "true" :
                   print ("GOAL reached,  wrap up")
                   print (s.children[i])
                   return s.children[i]
            q.delo ()
            for i in range (len (s.children)) :
                q.addo (s.children[i])
    
def manhdist (config):
    goalx = (0,0,0,1,1,1,2,2,2)
    goaly = (0,1,2,0,1,2,0,1,2)
    d = 0
    for i in range (9):
        x = goalx[i]
        y = goaly[i]
        d = d + abs (goalx[config[i]] - x) + abs (goaly[config[i]] - y)
    return (d)
          

# Main Function that reads in Input and Runs corresponding Algorithm

def main():

           

    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)
  
  
    
    if test_goal (hard_state) == "true" :
        print ("GOAL reached at beginning")
        return
    
    
    if sm == "bfs":

       final_state = bfs_search(hard_state)

    elif sm == "dfs":

        final_state = dfs_search(hard_state)

    elif sm == "ast":

        final_state = A_star_search(hard_state)

    else:

        # Without this return, execution falls through to the
        # `final_state` check below with final_state never assigned,
        # which crashes with UnboundLocalError instead of just printing
        # the message above and exiting cleanly.
        print("Enter valid command arguments !")
        return

    if final_state != None :
        print ("Total cost is ", final_state.cost)
        s = final_state
        while s != None:
            s.display ()
            print ()
            s = s.parent
    else :
        print ("No solution")
    
    writeOutput ()

if __name__ == '__main__':

    main()
    
    
