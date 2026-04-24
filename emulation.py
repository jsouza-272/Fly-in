from map import Map, Hub, Link
from drones import Drone
from algorithm import Astar


class SimulationEngine():
    def __init__(self, map: Map):
        self.__drones = map.drones
        self.__graph = map.map
        self.__start_hub = map.start_hub
        self.__end_hub = map.end_hub
        self.__map = map
