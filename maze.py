import random

TEST_RUNS_AMOUNT = 2
DIRECTION_BIAS = 0.4


with open("maze.txt") as f:
    maze = [list(line[:-1]) for line in f]


solution = None

for i in range(len(maze)):
    for j in range(len(maze[i])):
        if maze[i][j] == "x":
            solution = [i, j]
            break
            
MAZE_DIMENSIONS = (len(maze), len(maze[0]))
solution_coordinates = None
class Player:
    def __init__(self, starting_x=0, starting_y=0):
        self.current_position = {
            "x": starting_x,
            "y": starting_y
        }
        self.path_followed = []
        self.available_moves = {
            "up": True,
            "down": True,
            "left": True,
            "right": True
        }
        self.attempts_needed = 1
        


    def move_is_possible(self, direction):

        def is_not_wall(x, y):
            return maze[x][y] != "#"
        def is_within_bounds(x, y):
            return 0 <= x < MAZE_DIMENSIONS[0] and 0 <= y < MAZE_DIMENSIONS[1]
        def was_visited(x, y):
            return [x, y] in self.path_followed
        def was_previous_position(x, y):
            return [x, y] == self.path_followed[-1] if self.path_followed else False
        
        def destination_is_valid(x, y):
            if solution_coordinates is None:
                return is_within_bounds(x, y) and is_not_wall(x, y)
            else:
                # return not was_previous_position(x, y) and is_within_bounds(x, y) and is_not_wall(x, y)
                return not was_previous_position(x, y) and is_within_bounds(x, y) and is_not_wall(x, y) and not was_visited(x, y)
            # return not was_previous_position(x, y) and is_within_bounds(x, y) and is_not_wall(x, y)
        
        if direction == "up":
            return destination_is_valid(self.current_position["x"], self.current_position["y"] - 1)
        elif direction == "down":
            return destination_is_valid(self.current_position["x"], self.current_position["y"] + 1)
        elif direction == "left":
            return destination_is_valid(self.current_position["x"] - 1, self.current_position["y"])
        elif direction == "right":
            return destination_is_valid(self.current_position["x"] + 1, self.current_position["y"])

    def move(self, direction):
        # if self.move_is_possible(direction):
        self.path_followed.append([self.current_position["x"], self.current_position["y"]])
        if direction == "up":
            self.current_position["y"] -= 1
        elif direction == "down":
            self.current_position["y"] += 1
        elif direction == "left":
            self.current_position["x"] -= 1
        elif direction == "right":
            self.current_position["x"] += 1

    def check_available_moves(self):
        self.available_moves["up"] = self.move_is_possible("up")
        self.available_moves["down"] = self.move_is_possible("down")
        self.available_moves["left"] = self.move_is_possible("left")
        self.available_moves["right"] = self.move_is_possible("right")
            
    def exit_found(self):
        return [self.current_position["x"], self.current_position["y"]] == solution

record = None

def basic_algorithm(player=None, ):
    global record
    if player is None:
        player = Player()
    while True:
        player.check_available_moves()
        possible_directions = [direction for direction, is_possible in player.available_moves.items() if is_possible]
        
        if not possible_directions:
            player.path_followed = []
            player.current_position = {
                "x": 0,
                "y": 0
            }
            player.attempts_needed += 1
            continue
        
        if solution_coordinates is None or random.random() > DIRECTION_BIAS:
            chosen_direction = random.choice(possible_directions)
        else:
            chosen_direction = min(
                possible_directions,
                key=lambda direction: (
                    abs(player.current_position["x"] + (1 if direction == "right" else -1 if direction == "left" else 0) - solution_coordinates[0]) +
                    abs(player.current_position["y"] + (1 if direction == "down" else -1 if direction == "up" else 0) - solution_coordinates[1])
                )
            )
        player.move(chosen_direction)
        # for i in range(MAZE_DIMENSION):
        #     for j in range(MAZE_DIMENSION):
        #         if [i, j] in player.path_followed:
        #             print("·", end="")
        #         else:
        #             print(maze[i][j], end="")
                    
        #     print()

        if player.exit_found():

            player.path_followed.append([player.current_position["x"], player.current_position["y"]])
            if record is None:
                record = len(player.path_followed)
            else:
                if len(player.path_followed) > record:
                    # print("Longer than previous record.")
                    continue
                if record > len(player.path_followed):
                    record = len(player.path_followed)
                    print(f"New record: {record} steps.")
            print("Exit found!")
            break

    for i in range(MAZE_DIMENSIONS[0]):
        for j in range(MAZE_DIMENSIONS[1]):
            if [i, j] in player.path_followed[:-1]:
                print("·", end="")
            else:
                print(maze[i][j], end="")
                
        print()

    print()
    print(f"Steps: {len(player.path_followed)}")
    print(f"Attempts needed: {player.attempts_needed:>5}")
    return player.path_followed


def improve_run(previous_run, depth):
    first_half = previous_run[:depth]
    # first_half = previous_run[:len(previous_run)//2]
    player = Player()
    player.path_followed = first_half
    player.current_position = {
        "x": first_half[-1][0],
        "y": first_half[-1][1]
    }
    basic_algorithm(player)




def run_tests():
    global solution_coordinates
    test_runs = []

    for test_run in range(TEST_RUNS_AMOUNT):
        player = Player()
        while True:
            player.check_available_moves()
            possible_directions = [direction for direction, is_possible in player.available_moves.items() if is_possible]
            
            if not possible_directions:
                player.path_followed = []
                player.current_position = {
                    "x": 0,
                    "y": 0
                }
                player.attempts_needed += 1
                continue

            chosen_direction = random.choice(possible_directions)
            player.move(chosen_direction)

            if player.exit_found():
                if solution_coordinates is None:
                    solution_coordinates = [player.current_position["x"], player.current_position["y"]]
                player.path_followed.append([player.current_position["x"], player.current_position["y"]])
                test_runs.append(player.path_followed)
                print(f"Test run {test_run + 1} completed. {len(player.path_followed)} steps. {player.attempts_needed} attempts needed.")
                break

    shortest_run = min(test_runs, key=len)
    print(f"Shortest run found with {len(shortest_run)} steps.")
    return shortest_run



# previous_run = basic_algorithm()
shortest_run_from_tests = run_tests()
for i in range(2, len(shortest_run_from_tests)):
    print(f"Iteration {i}/{len(shortest_run_from_tests)}")
    improve_run(shortest_run_from_tests, i)
