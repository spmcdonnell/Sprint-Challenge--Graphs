from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

opposite_legend = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}


def get_opposite_direction(direction):
    return opposite_legend[direction]


def traverse_map():
    full_path = []
    visited = {}
    prev_room = []
    reverse_direction = ''

    while len(visited) < len(room_graph):

        current_location = player.current_room
        all_exits = player.current_room.get_exits()

        if len(full_path) > 0:
            reverse_direction = get_opposite_direction(full_path[-1])

        ##############################
        # Not visited yet
        ##############################
        if current_location.id not in list(visited):

            ### Set unvisited room exit data ###
            room_data = {}

            for direction in all_exits:
                room_data[direction] = '?'

            visited[current_location.id] = room_data

            ### Link current room direction that points to previous room ###
            if len(prev_room):
                visited[current_location.id][reverse_direction] = prev_room[-1]

            ### Gather available potential moves from current location ###
            possible_moves = []

            for key in visited[current_location.id]:
                possible_moves.append(visited[current_location.id][key])

            ##############################
            # If there are unknown paths
            ##############################
            if '?' in possible_moves:

                ### List paths from current room that are unknown ###
                unknown_paths = []

                for key in visited[current_location.id]:
                    if visited[current_location.id][key] == '?':
                        unknown_paths.append(key)

                ### Choose a random unknown path ###
                random_unknown = random.choice(unknown_paths)

                ### Keep track of last room before moving ###
                prev_room.append(current_location.id)

                ### Add to the path and then move there ###
                full_path.append(random_unknown)
                player.travel(random_unknown)

                ### Update the direction from the previous room so that it points to the room just moved to instead of '?' ###
                visited[current_location.id][random_unknown] = player.current_room.id

            ##############################
            # If all paths are known
            ##############################
            else:
                prev_room_direction = ''

                for key in visited[current_location.id]:
                    if visited[current_location.id][key] == prev_room[-1]:
                        prev_room_direction = key

                ### Add to the path and then move there ###
                full_path.append(prev_room_direction)
                player.travel(prev_room_direction)

                prev_room.pop()

        ##############################
        # Has been visited
        ##############################
        else:

            ### Gather available potential moves from current location ###
            possible_moves = []

            for key in visited[current_location.id]:
                possible_moves.append(visited[current_location.id][key])

            ##############################
            # If there are unknown paths
            ##############################
            if '?' in possible_moves:

                ### List paths from current room that are unknown ###
                unknown_paths = []

                for key in visited[current_location.id]:
                    if visited[current_location.id][key] == '?':
                        unknown_paths.append(key)

                ### Choose a random unknown path ###
                random_unknown = random.choice(unknown_paths)

                ### Keep track of last room before moving ###
                prev_room.append(current_location.id)

                ### Add to the path and then move there ###
                full_path.append(random_unknown)
                player.travel(random_unknown)

                ### Update the direction from the previous room so that it points to the room just moved to instead of '?' ###
                visited[current_location.id][random_unknown] = player.current_room.id

            ##############################
            # If all paths are known
            ##############################
            else:
                prev_room_direction = ''

                for key in visited[current_location.id]:
                    if visited[current_location.id][key] == prev_room[-1]:
                        prev_room_direction = key

                ### Add to the path and then move there ###
                full_path.append(prev_room_direction)
                player.travel(prev_room_direction)

                prev_room.pop()

    return full_path


traversal_path = traverse_map()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
