from map import Map, Hub, Link
from drones import DronesManager, Drone
from algorithm import Astar


class SimulationEngine():
    def __init__(self, map: Map, drones_manager: DronesManager):
        self.__drones = drones_manager.drones
        self.__drones_manager = drones_manager
        self.__graph = map.map
        self.__start_hub = map.start_hub
        self.__end_hub = map.end_hub
        self.__map = map

    def turn(self):
        i = 0
        drones = self.__drones
        d_manager = self.__drones_manager
        while len(drones) != len(d_manager.end_drones):
            turn_msg = ''
            i += 1
            for drone in drones:
                turn_msg += d_manager.move_drone(drone)
            print(turn_msg, i)
            if i == 5:
                break
