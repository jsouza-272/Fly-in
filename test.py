from parser import Parser
from mapbuilder.mapbuilder import MapBuilder


ccc = 'maps/challenger/01_the_impossible_dream.txt'
first = 'maps/easy/01_linear_path.txt'
hard = 'maps/hard/02_capacity_hell.txt'
parsing = Parser(hard)
try:
    config = parsing.parsing()
except Exception as e:
    print(e)
# config = Parser.parsing(first)
# map = MapBuilder(**config)
