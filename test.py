from parser import Parser
from mapbuilder.mapbuilder import MapBuilder
from algorithm.Astar import Astar
import sys


ccc = 'maps/challenger/01_the_impossible_dream.txt'
first = 'maps/easy/01_linear_path.txt'
hard = 'maps/hard/02_capacity_hell.txt'
hard2 = 'maps/hard//03_ultimate_challenge.txt'
try:
    parsing = Parser(first)
    config = parsing.parsing()
except Exception as e:
    print(e)
    sys.exit(1)
map = MapBuilder(**config)
print(Astar().algorithm(map))
