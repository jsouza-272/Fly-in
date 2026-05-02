from .drone import Drone
from map import Hub
from algorithm import Algorithm


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

    def create_drones(self, nb_drones: int, start_drone_position: Hub,
                      name_patern: str = 'D') -> None:
        self.__drones.extend([Drone(name_patern + str(n + 1),
                                    start_drone_position)
                              for n in range(nb_drones)])

    def set_drones_route(self, route: list[Hub]) -> None:
        if (not isinstance(route, list)
                or not all(isinstance(_, Hub) for _ in route)):
            raise TypeError('route must be a list of Hub objects')
        if not route:
            raise ValueError('route must not be empty')
        for drone in self.__drones:
            drone.route = route.copy()

    def recalculate_route(self, drone: Drone, algorithm: Algorithm) -> None:
        pass
