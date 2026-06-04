from typing import List, Dict, Tuple, Set
from collections import deque
import copy, heapq

class State:
    def __init__(self, pawn_position=None, puzzle=None, pawn_level=None, blank_position=None, g=0, parent=None, action=None):
        self.pawn_position = pawn_position
        self.puzzle = puzzle
        self.pawn_level = pawn_level
        self.blank_position = blank_position
        self.g = g
        self.f = 0
        self.parent = parent
        self.action = action 
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (
            self.pawn_position == other.pawn_position and
            self.blank_position == other.blank_position and
            self.pawn_level == other.pawn_level and
            self.puzzle == other.puzzle
        )
    def __hash__(self):
        return hash((tuple(map(tuple, self.puzzle)), self.pawn_position, self.blank_position, self.pawn_level))
    def __lt__(self, other):
        return self.f < other.f
    def __repr__(self):
        return f"State(pawn={self.pawn_position}, blank={self.blank_position}, level={self.pawn_level}, f={self.f})"



def heuristic(state: State):
    pawn_row = state.pawn_position // 3
    pawn_col = state.pawn_position % 3
    h = pawn_row + pawn_col
    tile_at_0 = tiles[state.puzzle[0][0]]
    if (state.pawn_level == "ground" and 4 not in tile_at_0.stairs) or 4 not in tile_at_0.top_opening:
        h += 2  
    return h


def get_exit_path(state: State) -> Tuple[bool, List[str], int]:
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    dir_names = ["up", "right", "down", "left"]
    queue = deque([(state.pawn_position, state.pawn_level, [])])
    visited = set([(state.pawn_position, state.pawn_level)])
    blank_row = state.blank_position // 3
    blank_col = state.blank_position % 3

    while queue:
        pawn_position, pawn_level, path = queue.popleft()
        pawn_row = pawn_position // 3
        pawn_col = pawn_position % 3
        
        if pawn_position == 0:
            first_tile = tiles[state.puzzle[0][0]]
            if pawn_level == "top" and 4 in first_tile.top_opening:
                exit_action = f"Exit from cell 0 (top) through left boundary (side 4)"
                return True, path + [exit_action], len(path) + 1
            if pawn_level == "ground" and 4 in first_tile.stairs:
                exit_action = f"Exit from cell 0 (ground) through left boundary (side 4) via stairs"
                return True, path + [exit_action], len(path) + 1
        
        curr_tile = tiles[state.puzzle[pawn_row][pawn_col]]
        for i, (dr, dc) in enumerate(directions):
            side = i + 1
            row, col = pawn_row + dr, pawn_col + dc
            if 0 <= row < 3 and 0 <= col < 3 and not (row == blank_row and col == blank_col):
                next_tile = tiles[state.puzzle[row][col]]
                opp_side = (side + 2) % 4 or 4
                next_pos = row * 3 + col

                if pawn_level == "ground":
                    if side in curr_tile.ground_opening and opp_side in next_tile.ground_opening:
                        if (next_pos, "ground") not in visited:
                            visited.add((next_pos, "ground"))
                            new_path = path + [f"Walk from cell {pawn_position} to {next_pos} (ground)"]
                            queue.append((next_pos, "ground", new_path))
                    if side in curr_tile.stairs and opp_side in next_tile.top_opening:
                        if (next_pos, "top") not in visited:
                            visited.add((next_pos, "top"))
                            new_path = path + [f"Climb from cell {pawn_position} (ground) to {next_pos} (top)"]
                            queue.append((next_pos, "top", new_path))
                elif pawn_level == "top":
                    if side in curr_tile.top_opening and opp_side in next_tile.top_opening:
                        if (next_pos, "top") not in visited:
                            visited.add((next_pos, "top"))
                            new_path = path + [f"Walk from cell {pawn_position} to {next_pos} (top)"]
                            queue.append((next_pos, "top", new_path))
                    if side in curr_tile.top_opening and opp_side in next_tile.stairs:
                        if (next_pos, "ground") not in visited:
                            visited.add((next_pos, "ground"))
                            new_path = path + [f"Descend from cell {pawn_position} (top) to {next_pos} (ground)"]
                            queue.append((next_pos, "ground", new_path))
    return False, [], 0

def can_reach_exit(state: State) -> bool:
    can_exit, _, _ = get_exit_path(state)
    return can_exit

def generate_neighbors_tile_change(state: State):
    directions = [[0, 1], [-1, 0], [0, -1], [1, 0]]
    dir_names = ["left", "down", "right", "up"]
    neighbors = []
    blank_row = state.blank_position // 3
    blank_col = state.blank_position % 3
    pawn_row = state.pawn_position // 3
    pawn_col = state.pawn_position % 3

    for idx in range(4):
        x, y = blank_row + directions[idx][0], blank_col + directions[idx][1]
        if 0 <= x < 3 and 0 <= y < 3:
            if x == pawn_row and y == pawn_col:
                continue
            tile_pos = x * 3 + y
            tile_name = state.puzzle[x][y]
            new_puzzle = copy.deepcopy(state.puzzle)
            new_puzzle[blank_row][blank_col], new_puzzle[x][y] = new_puzzle[x][y], new_puzzle[blank_row][blank_col]
            new_blank_index = tile_pos

            move_action = f"Slide '{tile_name}' from cell {tile_pos} to cell {state.blank_position}"

            new_state = State(
                pawn_position=state.pawn_position,
                puzzle=new_puzzle,
                pawn_level=state.pawn_level,
                blank_position=new_blank_index,
                g=state.g + 1,
                parent=state,
                action=move_action
            )
            new_state.f = new_state.g + heuristic(new_state)
            neighbors.append(new_state)
    return neighbors


def generate_pawn_change_neighbors(state):
    neighbors = []
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    dir_names = ["up", "right", "down", "left"]
    
    queue = deque([(state.pawn_position, state.pawn_level, [])])
    visited = set([(state.pawn_position, state.pawn_level)])
    blank_row = state.blank_position // 3
    blank_col = state.blank_position % 3

    while queue:
        curr_pos, curr_level, path_actions = queue.popleft()
        pawn_row = curr_pos // 3
        pawn_col = curr_pos % 3
        curr_tile = tiles[state.puzzle[pawn_row][pawn_col]]

        for i in range(4):
            side = i + 1
            row = pawn_row + directions[i][0]
            col = pawn_col + directions[i][1]
            
            if not (0 <= row < 3 and 0 <= col < 3) or (row == blank_row and col == blank_col):
                continue

            next_tile = tiles[state.puzzle[row][col]]
            opp_side = (side + 2) % 4 or 4
            next_pos = row * 3 + col

            if curr_level == "ground":
                if side in curr_tile.ground_opening and opp_side in next_tile.ground_opening:
                    if (next_pos, "ground") not in visited:
                        visited.add((next_pos, "ground"))
                        new_path = path_actions + [f"Walk from cell {curr_pos} to {next_pos} (ground)"]
                        queue.append((next_pos, "ground", new_path))
                        if next_tile.hole:
                            new_state = State(
                                pawn_position=next_pos,
                                puzzle=copy.deepcopy(state.puzzle),
                                pawn_level="ground",
                                blank_position=state.blank_position,
                                g=state.g + len(new_path),
                                parent=state,
                                action=" → ".join(new_path)
                            )
                            new_state.f = new_state.g + heuristic(new_state)
                            neighbors.append(new_state)

                if side in curr_tile.stairs and opp_side in next_tile.top_opening:
                    if (next_pos, "top") not in visited:
                        visited.add((next_pos, "top"))
                        new_path = path_actions + [f"Climb from cell {curr_pos} (ground) to {next_pos} (top)"]
                        queue.append((next_pos, "top", new_path))
                        if next_tile.hole:
                            new_state = State(
                                pawn_position=next_pos,
                                puzzle=copy.deepcopy(state.puzzle),
                                pawn_level="top",
                                blank_position=state.blank_position,
                                g=state.g + len(new_path),
                                parent=state,
                                action=" → ".join(new_path)
                            )
                            new_state.f = new_state.g + heuristic(new_state)
                            neighbors.append(new_state)

            elif curr_level == "top":
                if side in curr_tile.top_opening and opp_side in next_tile.top_opening:
                    if (next_pos, "top") not in visited:
                        visited.add((next_pos, "top"))
                        new_path = path_actions + [f"Walk from cell {curr_pos} to {next_pos} (top)"]
                        queue.append((next_pos, "top", new_path))
                        if next_tile.hole:
                            new_state = State(
                                pawn_position=next_pos,
                                puzzle=copy.deepcopy(state.puzzle),
                                pawn_level="top",
                                blank_position=state.blank_position,
                                g=state.g + len(new_path),
                                parent=state,
                                action=" → ".join(new_path)
                            )
                            new_state.f = new_state.g + heuristic(new_state)
                            neighbors.append(new_state)

                if side in curr_tile.top_opening and opp_side in next_tile.stairs:
                    if (next_pos, "ground") not in visited:
                        visited.add((next_pos, "ground"))
                        new_path = path_actions + [f"Descend from cell {curr_pos} (top) to {next_pos} (ground)"]
                        queue.append((next_pos, "ground", new_path))
                        if next_tile.hole:
                            new_state = State(
                                pawn_position=next_pos,
                                puzzle=copy.deepcopy(state.puzzle),
                                pawn_level="ground",
                                blank_position=state.blank_position,
                                g=state.g + len(new_path),
                                parent=state,
                                action=" → ".join(new_path)
                            )
                            new_state.f = new_state.g + heuristic(new_state)
                            neighbors.append(new_state)
    return neighbors


def generate_neighbors(state: State):
    neighbors = []
    neighbors.extend(generate_neighbors_tile_change(state))
    neighbors.extend(generate_pawn_change_neighbors(state))
    return neighbors


def goal_check(state: State) -> bool:
    return can_reach_exit(state)


def reconstruct_path(state):
    path = []
    while state:
        path.append(state)
        state = state.parent
    return list(reversed(path))


def print_solution(path):
    if not path:
        print("No solution found")
        return
    
    print("\n" + "=" * 80)
    print("SOLUTION FOUND!")
    print("=" * 80)
    
    final_state = path[-1]
    can_exit, exit_path, exit_cost = get_exit_path(final_state)
    total_cost = final_state.g + exit_cost
    
    print(f"Total cost (including exit): {total_cost}")
    print(f"Number of configuration steps: {len(path) - 1}")
    print(f"Number of exit movement steps: {exit_cost}\n")

    for i, state in enumerate(path):
        print("=" * 80)
        print(f"Step {i}:")
        if state.action:
            print(f"Action: {state.action}")
        else:
            print("Action: Initial State")
        print(f"Cost so far: {state.g}")
        print(f"Pawn: Cell {state.pawn_position} ({state.pawn_level}), Blank: Cell {state.blank_position}")
        print("\nPuzzle Grid:")
        for r in range(3):
            row_str = "  "
            for c in range(3):
                idx = r * 3 + c
                tile = state.puzzle[r][c]
                if idx == state.pawn_position:
                    row_str += f"[{tile}*] "
                elif idx == state.blank_position:
                    row_str += f"[ - ] "
                else:
                    row_str += f" {tile}   "
            print(row_str)
        print()

    if can_exit and exit_path:
        print("=" * 80)
        print("EXIT MOVEMENTS:")
        print("=" * 80)
        for i, move in enumerate(exit_path, 1):
            print(f"Exit Step {i}: {move}")
            print(f"Cost so far: {final_state.g + i}")
        print()
    
    print("=" * 80)
    print(f"FINAL TOTAL COST: {total_cost}")
    print("*** GOAL REACHED! Pawn has successfully escaped the temple! ***")
    print("=" * 80 + "\n")


def astar(start_state: State):
    start_state.f = start_state.g + heuristic(start_state)
    open_set = [start_state]
    visited = set()
    
    while open_set:
        current = heapq.heappop(open_set)
        
        if goal_check(current):
            return reconstruct_path(current)
        
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor in generate_neighbors(current):
            if neighbor not in visited:
                heapq.heappush(open_set, neighbor)
    
    return None


class Tile:
    def __init__(self, shape=None, top_opening=None, ground_opening=None, hole=False, stairs=None):
        self.shape = shape
        self.top_opening = top_opening if top_opening else []
        self.ground_opening = ground_opening if ground_opening else []
        self.hole = hole
        self.stairs = stairs if stairs else []


    def __repr__(self):
        return f"Tile({self.shape}, top={self.top_opening}, ground={self.ground_opening}, hole={self.hole}, stairs={self.stairs})"


tiles_orginal = {
    'A': Tile('=', top_opening=[1, 2], ground_opening=[], hole=False, stairs=[]),
    'B': Tile('sq', top_opening=[1, 2], ground_opening=[], hole=False, stairs=[]),
    'C': Tile('+', top_opening=[2, 4], ground_opening=[], hole=False, stairs=[]),
    'D': Tile('rb', top_opening=[4], ground_opening=[2], hole=True, stairs=[4]),
    'E': Tile('*', top_opening=[4], ground_opening=[2], hole=True, stairs=[4]),
    'F': Tile('>', top_opening=[], ground_opening=[1, 2], hole=True, stairs=[]),
    'G': Tile('x', top_opening=[], ground_opening=[1, 2], hole=True, stairs=[]),
    'H': Tile('.', top_opening=[], ground_opening=[1,2], hole=True, stairs=[]),
    '-': Tile('-', top_opening=[], ground_opening=[], hole=False, stairs=[]),  # Blank
}


levels = {
    'starter-1': {
        'board': ['C', 'D', 'G', 'B', '-', 'H', 'A', 'E', 'F'],
        'pawn_pos': 8,
        'blank_pos':4,
        'pawn_level':"ground",
        'orientation': [0, 0, 2, 1, 0, 3, 0, 0, 2] 
    },
    'starter-2': {
        'board': ['A', 'E', 'G', 'B', '-', 'D', 'H', 'C', 'F'],
        'pawn_pos': 1,
        'blank_pos':4,
        'pawn_level':"ground",
        'orientation': [2, 3, 0, 0, 0, 0, 0, 0, 2]
    },
    'starter-3': {
        'board': ['G', 'E', 'B', 'D', 'H', 'F', 'A', '-', 'C'],
        'pawn_pos': 1,
        'blank_pos':7,
        'pawn_level':"ground",
        'orientation': [2, 1, 3, 0, 3, 0, 0, 0, 0]
    },
    'starter-4': {
        'board': ['B', 'D', 'H', 'E', 'G', 'F', '-', 'A', 'C'],
        'pawn_pos': 3,
        'blank_pos':6,
        'pawn_level':"ground",
        'orientation': [1, 0, 2, 1, 0, 3, 0, 0, 3]
    },
    'junior-1': {
        'board': ['G', 'F', 'E', 'A', 'B', 'C', 'H', '-', 'D'],
        'pawn_pos': 6,
        'blank_pos':7,
        'pawn_level':"ground",
        'orientation': [2, 1, 3, 2, 1, 0, 0, 0, 1]
    },
    'junior-2': {
        'board': ['C', 'E', 'G', 'F', '-', 'D', 'H', 'B', 'A'],
        'pawn_pos': 5,
        'blank_pos':4,
        'pawn_level':"ground",
        'orientation': [0, 0, 1, 0, 0, 2, 0, 3, 1]
    },
    'junior-3': {
        'board': ['C', 'A', 'B', 'D', 'E', 'G', '-', 'F', 'H'],
        'pawn_pos': 3,
        'blank_pos':6,
        'pawn_level':"ground",
        'orientation': [0, 0, 2, 2, 0, 2, 0, 2, 1]
    },
    'junior-4': {
        'board': ['G', 'H', 'C', 'B', '-', 'D', 'A', 'E', 'F'],
        'pawn_pos': 7,
        'blank_pos':4,
        'pawn_level':"ground",
        'orientation': [2, 0, 0, 1, 0, 0, 0, 0, 2]
    },
    'expert-1': {
        'board': ['D', 'B', 'C', 'G', 'F', 'A', 'H', 'E', '-'],
        'pawn_pos': 0,
        'blank_pos':8,
        'pawn_level':"ground",
        'orientation': [1, 2, 0, 0, 2, 3, 3, 3, 0]
    },
    'expert-2': {
        'board': ['B', 'A', 'D', 'C', 'F', 'G', '-', 'H', 'E'],
        'pawn_pos': 4,
        'blank_pos':6,
        'pawn_level':"ground",
        'orientation': [2, 0, 1, 3, 2, 1, 0, 3, 3]
    },
    'expert-3': {
        'board': ['C', 'A', '-', 'B', 'H', 'D', 'E', 'G', 'F'],
        'pawn_pos': 5,
        'blank_pos':2,
        'pawn_level':"ground",
        'orientation': [1, 2, 0, 0, 1, 2, 0, 0, 2]
    },
    'expert-4': {
        'board': ['B', 'D', 'F', 'A', 'E', 'G', 'H', 'C', '-'],
        'pawn_pos': 5,
        'blank_pos':8,
        'pawn_level':"ground",
        'orientation': [1, 0, 2, 0, 0, 2, 0, 0, 0]
    },
    'master-1': {
        'board': ['G', 'E', 'D', 'B', '-', 'F', 'A', 'H', 'C'],
        'pawn_pos': 7,
        'blank_pos':4,
        'pawn_level':"ground",
        'orientation': [1,2,0,2,0,3,0,0,3]
    },
    'master-2': {
        'board': ['E', 'G', 'F', '-', 'H', 'D', 'A', 'B', 'C'],
        'pawn_pos': 2,
        'blank_pos':3,
        'pawn_level':"ground",
        'orientation': [1,1,2,0,3,3,1,2,1]
    },
    '43': {
        'board': ['A', 'F', 'E', 'C', 'G', 'H', 'B', '-', 'D'],
        'pawn_pos': 4,
        'blank_pos':7,
        'pawn_level':"ground",
        'orientation': [0,2,1,0,1,2,2,0,3]
    },
    '55': {
        'board': ['A', 'G', 'B', 'F', 'D', 'E', '-', 'C', 'H'],
        'pawn_pos': 5,
        'blank_pos':6,
        'pawn_level':"ground",
        'orientation': [1,1,2,1,2,0,0,2,0]
    },


}



def update_tile_orientations(tiles:Tile, orientation,board, verbose=False):
    oriented_tiles ={}
    for i in range(9):
        variable = b[i]
        steps = orientation[i]
        if(variable=='-'):
            oriented_tiles['-']=tiles['-']
            continue
        top_opening  = tiles[variable].top_opening
        ground_opening = tiles[variable].ground_opening
        stairs = tiles[variable].stairs
        shape = tiles[variable].shape
        hole = tiles[variable].hole
        top_opening = [((j+steps)%4 or 4) for j in top_opening]
        ground_opening = [((j+steps)%4 or 4) for j in ground_opening]
        stairs= [((j+steps)%4 or 4) for j in stairs]
        oriented_tiles[variable]=Tile(top_opening=top_opening,ground_opening=ground_opening,shape=shape,stairs=stairs,hole=hole)
    return oriented_tiles

puzzle_level = '55'
b = levels[puzzle_level]['board']
orentations = levels[puzzle_level]['orientation']
start_puzzle = [[b[0],b[1],b[2]],[b[3],b[4],b[5]],[b[6],b[7],b[8]]]
pawn_pos = levels[puzzle_level]["pawn_pos"]
blank_pos = levels[puzzle_level]["blank_pos"]
pawn_level = levels[puzzle_level]["pawn_level"]

tiles = update_tile_orientations(tiles_orginal,orentations,b)
start_state = State(pawn_position=pawn_pos, puzzle=start_puzzle, pawn_level=pawn_level, blank_position=blank_pos)
path = astar(start_state)
print_solution(path)