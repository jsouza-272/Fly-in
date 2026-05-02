from map import Map, Hub, Link
from drones import DronesManager, Drone
from algorithm import Astar


class SimulationEngine():
    def __init__(self, map: Map, drones_manager: DronesManager):
        self.__drones = drones_manager.drones
        self.__graph = map.map
        self.__start_hub = map.start_hub
        self.__end_hub = map.end_hub
        self.__map = map

    def turn(self):
        pass
