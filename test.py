from parser import Parser
from map.map import Map
from algorithm.Astar import Astar
import sys


ccc = 'maps/challenger/01_the_impossible_dream.txt'
first = 'maps/easy/01_linear_path.txt'
hard = 'maps/hard/02_capacity_hell.txt'
hard2 = 'maps/hard/03_ultimate_challenge.txt'
try:
    parsing = Parser(hard)
    config = parsing.parsing()
except Exception as e:
    print(e)
    sys.exit(1)
map = Map(**config)
map.set_drone_destination(Astar().algorithm(map))
drones = map.drones
map.turn()
# print(Astar().algorithm(map))
