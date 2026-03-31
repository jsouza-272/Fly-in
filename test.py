from parser import Parser
from mapbuilder.mapbuilder import MapBuilder

ccc = 'maps/challenger/01_the_impossible_dream.txt'
first = 'maps/easy/01_linear_path.txt'
config = Parser.parsing(first)
map = MapBuilder(**config)
