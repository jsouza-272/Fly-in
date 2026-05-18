from map import Map, Hub
from drones import DronesManager, Drone
from copy import deepcopy
import time


class SimulationEngine():
    """Controls simulation turn execution."""

    def __init__(self, map: Map, drones_manager: DronesManager):
        """Initializes map and drone manager references."""
        self.__drones = drones_manager.drones
        self.__drones_manager = drones_manager
        self.__graph = map.map
        self.__map = map

    def turn(self) -> list[tuple[list[Hub], list[Drone]]]:
        """Runs turns until all drones arrive or timeout is reached."""
        start = time.time()
        turn_counter = 0
        drones = self.__drones
        d_manager = self.__drones_manager
        turns = []
        while len(drones) != len(d_manager.end_drones):
            turns.append((deepcopy(self.__graph), deepcopy(self.__drones)))
            turn_msg = ''
            turn_counter += 1
            for drone in drones:
                turn_msg += d_manager.move_drone(drone)
            print(turn_msg)
            self.__map.reset_links()
            if time.time() - start >= 1:
                print('time out')
                break
        turns.append((deepcopy(self.__graph), deepcopy(self.__drones)))
        print(turn_counter)
        return turns
