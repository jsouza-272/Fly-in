from .drone import Drone
from map import Hub


class DronesManager():
    """Gerencia coleção de drones e movimentação por rota."""

    def __init__(self, nb_drones: int = 0,
                 start_drone_position: Hub | None = None,
                 name_patern: str = 'D', create_drones: bool = False,
                 route: list[Hub] = []) -> None:
        """Inicializa gerenciador e opcionalmente cria drones iniciais."""
        self.__drones: list[Drone] = []
        self.__route: list[Hub] | None = None
        self.route = route
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
        """Retorna a lista de drones gerenciados."""
        return self.__drones

    @property
    def route(self) -> list[Hub] | None:
        """Retorna a rota atual utilizada pelos drones."""
        return self.__route

    @route.setter
    def route(self, new_route: list[Hub]) -> None:
        """Define a rota dos drones após validação de tipo."""
        if (isinstance(new_route, list)
                and all(isinstance(_, Hub) for _ in new_route)):
            self.__route = new_route
        else:
            raise TypeError('route must be a list of Hub objects')

    @property
    def moving_drones(self) -> list[Drone]:
        """Retorna somente os drones que estão se movendo."""
        return [d for d in self.drones if d.moving]

    @property
    def end_drones(self) -> list[Drone]:
        """Retorna drones que já chegaram ao hub final da rota."""
        return [d for d in self.__drones if self.route
                and d.node == self.route[0]]

    def create_drones(self, nb_drones: int, start_drone_position: Hub,
                      name_patern: str = 'D') -> None:
        """Cria drones no hub inicial com padrão de nome informado."""
        self.__drones.extend([Drone(name_patern + str(n + 1),
                                    start_drone_position)
                              for n in range(nb_drones)])
        start_drone_position.drones.extend(self.__drones)

    def move_drone(self, drone: Drone) -> str:
        """Avança um drone um passo na rota e retorna mensagem de movimento."""
        msg = ''
        if (isinstance(drone, Drone) and self.route
                and drone.node != self.route[0]):
            if drone.node:
                drone_index = self.route.index(drone.node)
            elif drone.old_node:
                drone_index = self.route.index(drone.old_node)
            node = self.route[drone_index-1]
            link = node.links.get((node, drone.node))
            msg = drone.move(node, link)
        return msg
