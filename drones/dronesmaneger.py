from .drone import Drone
from map import Hub, Map
from algorithm import Algorithm
from errors import RecalculateRoute, AlgorithmError


class DronesManager():
    def __init__(self, nb_drones: int = 0,
                 start_drone_position: Hub | None = None,
                 name_patern: str = 'D', create_drones: bool = False) -> None:
        self.__drones: list[Drone] = []
        if create_drones:
            if not start_drone_position:
                raise TypeError('if create_drones is True, '
                                'start_drone_position must be provided')
            if nb_drones < 1:
                raise ValueError('if create_drones is True, '
                                 'nb_drones must be greater than 0')
            self.create_drones(nb_drones, start_drone_position, name_patern)

    @property
    def drones(self) -> list[Drone]:
        return self.__drones

    @property
    def moving_drones(self) -> list[Drone]:
        return [d for d in self.drones if d.moving]

    @property
    def end_drones(self) -> list[Drone]:
        return [d for d in self.__drones if len(d.route) == 0]

    def create_drones(self, nb_drones: int, start_drone_position: Hub,
                      name_patern: str = 'D') -> None:
        self.__drones.extend([Drone(name_patern + str(n + 1),
                                    start_drone_position)
                              for n in range(nb_drones)])
        start_drone_position.drones.extend(self.__drones)

    def set_drones_route(self, route: list[Hub]) -> None:
        if (not isinstance(route, list)
                or not all(isinstance(_, Hub) for _ in route)):
            raise TypeError('route must be a list of Hub objects')
        if not route:
            raise ValueError('route must not be empty')
        for drone in self.__drones:
            drone.route = route.copy()

    def recalculate_route(self, drone: Drone,
                          algorithm: Algorithm, map: Map) -> bool:
        if drone.moving:
            return False
        try:
            new_route = algorithm.algorithm(map, [drone.route[-1]], drone.node)
            if new_route[:-1] == drone.route:
                return False
            if len(new_route[:-1]) <= len(drone.route) + 2:
                print(drone.node, drone.moving, new_route)
                drone.route = new_route
                return True
            else:
                return False
        except AlgorithmError:
            return False

    def move_drone(self, drone: Drone, try_recalc_route: bool = True) -> str:
        drone_move_info = None
        msg = ''
        if isinstance(drone, Drone) and len(drone.route) > 0:
            node = drone.route[-1]
            link = node.links.get((node, drone.node))
            if try_recalc_route and (not node.free() or not link.can_use()):
                raise RecalculateRoute()
            drone_move_info = drone.move(node, link)
            msg = drone_move_info[0]
            if drone_move_info[1] and drone_move_info[1] in drone.route:
                drone.route.remove(drone_move_info[1])
        return msg
