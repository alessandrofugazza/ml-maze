import random

TEST_RUNS_AMOUNT = 20


with open("maze.txt") as f:
    maze = [list(line[:-1]) for line in f]

SOLUTION = [len(maze) -1, len(maze) -1]
MAZE_DIMENSION = len(maze)

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
            return 0 <= x < MAZE_DIMENSION and 0 <= y < MAZE_DIMENSION
        def was_visited(x, y):
            return [x, y] in self.path_followed
        def was_previous_position(x, y):
            return [x, y] == self.path_followed[-1] if self.path_followed else False
        
        def destination_is_valid(x, y):
            return not was_previous_position(x, y) and is_within_bounds(x, y) and is_not_wall(x, y) and not was_visited(x, y)
        
        if direction == "up":
            return destination_is_valid(self.current_position["x"], self.current_position["y"] - 1)
        elif direction == "down":
            return destination_is_valid(self.current_position["x"], self.current_position["y"] + 1)
        elif direction == "left":
            return destination_is_valid(self.current_position["x"] - 1, self.current_position["y"])
        elif direction == "right":
            return destination_is_valid(self.current_position["x"] + 1, self.current_position["y"])

    def move(self, direction):
        if self.move_is_possible(direction):
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
        return [self.current_position["x"], self.current_position["y"]] == SOLUTION

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

        chosen_direction = random.choice(possible_directions)
        player.move(chosen_direction)

        if player.exit_found():

            player.path_followed.append([player.current_position["x"], player.current_position["y"]])
            if record is None:
                record = len(player.path_followed)
            else:
                if len(player.path_followed) > record:
                    print("Longer than previous record.")
                    continue
                if record > len(player.path_followed):
                    record = len(player.path_followed)
                    print(f"New record: {record} steps.")
            print("Exit found!")
            break

    for i in range(MAZE_DIMENSION):
        for j in range(MAZE_DIMENSION):
            if [i, j] in player.path_followed:
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

previous_run = basic_algorithm()
for i in range(2, len(previous_run)):
    improve_run(previous_run, i)


def run_tests():
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
                player.path_followed.append([player.current_position["x"], player.current_position["y"]])
                test_runs.append(player.path_followed)
                print(f"Test run {test_run + 1} completed. {len(player.path_followed)} steps. {player.attempts_needed} attempts needed.")
                break



# for test_run in test_runs:
#     print(test_run)