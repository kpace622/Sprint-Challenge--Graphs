from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# commit
# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

Checked = {}
list = []
exited = player.current_room.get_exits()
temp = {}
for i in range(len(exited)):
    temp.update({exited[i]: '?'})
Checked[player.current_room.id] = temp

while len(Checked) < len(room_graph) - 1:
    if player.current_room.id not in Checked:
        temp = {}
        exited = player.current_room.get_exits()
        for i in range(len(exited)):
            temp.update({exited[i]: '?'})
        Checked[player.current_room.id] = temp
        Checked[player.current_room.id][list[-1]] = player.current_room.get_room_in_direction(list[-1])
    current_path = []
    for exit_path, room in Checked[player.current_room.id].items():
        if room == '?': current_path.append(exit_path)

    while len(current_path) == 0 and len(list) > 0:
        reversed_direction = list.pop()
        traversal_path.append(reversed_direction)
        player.travel(reversed_direction)
        new_paths = []
        for exit_path, room in Checked[player.current_room.id].items():
            if room == '?':
                new_paths.append(exit_path)
        current_path = new_paths

    Checked[player.current_room.id][current_path[-1]] = player.current_room.get_room_in_direction(current_path[-1])
    move = current_path.pop()
    traversal_path.append(move)
    opposites = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
    list.append(opposites[move])
    player.travel(move)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
