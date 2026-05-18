"""Application entry point for loading maps and running the simulation UI."""

import sys
from parser import Parser
from map import Map
from drones import DronesManager
from algorithm import Dijkstra
from emulation import SimulationEngine
import os
from Gui import Gui


def main(debug: bool, path: str) -> str:
    """Loads configuration and starts the GUI simulation loop."""
    try:
        if len(sys.argv) < 2:
            raise SyntaxError('Usage: python3 fly_in.py <map_path.txt>')
        if not debug:
            path = sys.argv[1]
        parsing = Parser(path)
        config = parsing.parsing()
    except Exception as e:
        print(e)
        sys.exit(1)
    map = Map(**config)
    drones_manager = DronesManager(config['nb_drones'], map.start_hub,
                                   create_drones=True)
    drones_manager.route = Dijkstra().algorithm(map)
    engine = SimulationEngine(map, drones_manager)
    print('nb_drones:', config['nb_drones'])
    interface = Gui(map, path.split('/', maxsplit=1)[-1], engine)
    return interface.loop(debug)


if __name__ == "__main__":
    debug = '--debug' in sys.argv
    user_input = ""
    i = 0
    if debug:
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
    else:
        path_list = []
    while user_input != 'q':
        os.system("clear")
        if debug and user_input == 'b':
            if i > 0:
                i -= 1
        if debug and user_input == 'n':
            i += 1
        if debug and i == len(path_list):
            print('END')
            break
        if debug and path_list:
            path = path_list[i]
        else:
            path = ''
        user_input = main(debug, path)
