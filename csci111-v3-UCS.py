import heapq
import random
from collections import deque

#[6, 0, 8]
#[5, 3, 2]
#[4, 7, 1]

#Reference work: https://gist.github.com/Hossam-Elbahrawy/391f060242e7203702da0843fd523d4f
#initial state generator (to avoid making impossible combinations)

def count_inversions(state):
    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                inversions += 1
    return inversions

#states are solvable if inversions are even, unsolvable if odd
def is_solvable(state):
    inversions = count_inversions(state)
    return inversions % 2 == 0

def create_solvable_state(goal_state):
    shuffled_state = goal_state[:]
    while True:
        random.shuffle(shuffled_state)
        if is_solvable(shuffled_state):
            return shuffled_state

def get_user_goal_state():
    while True:
        user_input = input("goal state: ")
        
        if user_input.lower() == 'x':  
            return None

        if user_input.lower() == 'default':
            user_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
            return user_state
        
        user_state = list(map(int, user_input.split()))
        if len(user_state) == 9 and all(0 <= x <= 8 for x in user_state) and len(set(user_state)) == 9:
            return user_state
        else:
            print("invalid")

#for the actual 8-puzzle itself

def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])

def get_neighbors(state):
    neighbors = []
    blank_pos = state.index(0)
    row, col = blank_pos // 3, blank_pos % 3
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_pos = new_row * 3 + new_col
            new_state = state[:]
            new_state[blank_pos], new_state[new_blank_pos] = new_state[new_blank_pos], new_state[blank_pos]
            neighbors.append(new_state)
    
    return neighbors

def uniform_cost_search(initial_state, goal_state):
    frontier = [(0, initial_state, [])]
  
    visited = set()
    visited.add(tuple(initial_state))


    while frontier:
        cost, current_state, path = heapq.heappop(frontier)
        if current_state == goal_state:
            #print("goal found")
            return path

        neighbors = get_neighbors(current_state)      
        for neighbor in neighbors:
            if tuple(neighbor) not in visited:
                visited.add(tuple(neighbor))  
                new_cost = cost + 1 #all moves for UCS cost 1
                new_path = path + [neighbor] 
                
                heapq.heappush(frontier, (new_cost, neighbor, new_path))

    return None #no solution

def breadth_first_search(initial_state, goal_state):
    frontier = deque([(initial_state, [])])
    
    visited = set()
    visited.add(tuple(initial_state))
    
    while frontier:
        current_state, path = frontier.popleft() # dequeue the next state (FIFO)
        
        if current_state == goal_state:
            #print("goal found")
            return path

        neighbors = get_neighbors(current_state)
        for neighbor in neighbors:
            if tuple(neighbor) not in visited:
                visited.add(tuple(neighbor))
                new_path = path + [neighbor]
                frontier.append((neighbor, new_path))
                
def depth_first_search(initial_state, goal_state):
    frontier = [(initial_state, [])]

    visited = set()
    
    while frontier:
        current_state, path = frontier.pop() # pop the next state (LIFO)

        if current_state == goal_state:
            #print("goal found")
            return path
        
        visited.add(tuple(current_state))

        neighbors = get_neighbors(current_state)
        for neighbor in neighbors:
            if tuple(neighbor) not in visited:
                new_path = path + [neighbor]
                frontier.append((neighbor, new_path))

    return None #no solution

# , 3, 8, 5, 0, 2, 4, 7, 1]
#goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

while True:
    goal_state = get_user_goal_state()

    if goal_state is None:  
        print("closing...")
        break

    initial_state = create_solvable_state(goal_state)

    print("Initial State:")
    print_puzzle(initial_state)
    print("\nGoal State:")
    print_puzzle(goal_state)

    # Choose an algorithm
    algorithm_choice = input("\nChoose an algorithm (ucs, bfs, or dfs):")
    
    if algorithm_choice =='ucs':
        solution = uniform_cost_search(initial_state, goal_state)
    elif algorithm_choice =='bfs':
        solution = breadth_first_search(initial_state, goal_state)
    elif algorithm_choice =='dfs':
        solution = depth_first_search(initial_state, goal_state)
    else:
        print("Invalid choice")
        continue

    if solution:
        print("\nSolution exists")
        move_number = 1
        for state in solution:
            print(f"\nMove {move_number}:")
            print_puzzle(state)
            move_number += 1
    else:
        print("\nNo solution")

    print("\n\n")
