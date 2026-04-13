from parser import Parser
from mapbuilder.mapbuilder import MapBuilder
from algorithm.Astar import Astar
import sys


ccc = 'maps/challenger/01_the_impossible_dream.txt'
first = 'maps/easy/01_linear_path.txt'
hard = 'maps/hard/02_capacity_hell.txt'
hard2 = 'maps/hard//03_ultimate_challenge.txt'
try:
    parsing = Parser(hard)
    config = parsing.parsing()
except Exception as e:
    print(e)
    sys.exit(1)
map = MapBuilder(**config)
drones = map.drones
algorithm = Astar()
solve = algorithm.algorithm(map)
print(solve)

i = len(solve) - 1
while drones:
    result = ''
    if i < 0:
        i = len(solve) - 1
    for drone in drones:
        if i + 1 < len(solve) - 1 and any(d.node == solve[i] for d in drones):
            result += drone.move(solve[i + 1])
        else:
            result += drone.move(solve[i])
    for drone in drones:
        if drone.node == solve[0]:
            drones.remove(drone)
            drone.node.drones.remove(drone)
    i -= 1
    if result:
        print(result)
