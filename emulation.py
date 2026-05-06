from map import Map, Hub, Link
from drones import DronesManager, Drone
from algorithm import Astar
from errors.anyerrors import RecalculateRoute


class SimulationEngine():
    def __init__(self, map: Map, drones_manager: DronesManager):
        self.__drones = drones_manager.drones
        self.__drones_manager = drones_manager
        self.__graph = map.map
        self.__start_hub = map.start_hub
        self.__end_hub = map.end_hub
        self.__map = map

    def turn(self):
        turn_counter = 0
        drones = self.__drones
        d_manager = self.__drones_manager
        while len(drones) != len(d_manager.end_drones):
            turn_msg = ''
            turn_counter += 1
            for drone in drones:
                try:
                    turn_msg += d_manager.move_drone(drone)
                except RecalculateRoute:
                    recalculate_result = d_manager.recalculate_route(
                        drone, Astar(), self.__map)
                    if recalculate_result:
                        turn_msg += d_manager.move_drone(drone, False)
                    else:
                        turn_msg += d_manager.move_drone(drone, False)
            print(turn_msg)
            self.__map.reset_links()
        print(turn_counter)
