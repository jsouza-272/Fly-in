import sys
from parser import Parser
from map import Map, Hub, Link
from drones import DronesManager
from algorithm import Astar
from emulation import SimulationEngine
import os
from Gui import Gui


def bloom(path: str):
    try:
        parsing = Parser(path)
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
    print('nb_drones:', config['nb_drones'])
    interface = Gui(map, path.split('/', maxsplit=1)[-1])
    return interface.loop()


user_input = 'n'
i = 0
path_list = [
    'maps/easy/01_linear_path.txt',
    'maps/easy/02_simple_fork.txt',
    'maps/easy/03_basic_capacity.txt',
    'maps/medium/01_dead_end_trap.txt',
    'maps/medium/02_circular_loop.txt',
    'maps/medium/03_priority_puzzle.txt',
    'maps/hard/01_maze_nightmare.txt',
    'maps/hard/02_capacity_hell.txt',
    'maps/hard/03_ultimate_challenge.txt',
    'maps/challenger/01_the_impossible_dream.txt'
]
while user_input != 'q':
    os.system("clear")
    if user_input == 'b':
        if i > 0:
            i -= 1
            user_input = 'n'
    if i == len(path_list):
        print('END')
        break
    if user_input == 'n':
        user_input = bloom(path_list[i])
        i += 1
