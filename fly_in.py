import sys
from parser import Parser
from map import Map, Hub, Link
from drones import DronesManager
from algorithm import Astar
from emulation import SimulationEngine
# from Gui import Gui


ccc = 'maps/challenger/01_the_impossible_dream.txt'
first = 'maps/easy/01_linear_path.txt'
hard = 'maps/hard/02_capacity_hell.txt'
hard2 = 'maps/hard/03_ultimate_challenge.txt'
try:
    parsing = Parser(first)
    config = parsing.parsing()
except Exception as e:
    print(e)
    sys.exit(1)
map = Map(**config)
drones_manager = DronesManager(config['nb_drones'], map.start_hub,
                               create_drones=True)
drones_manager.set_drones_route(Astar().algorithm(map))
engine = SimulationEngine(map, drones_manager)
engine.turn()
# interface = Gui(map)
# interface.loop()
