from map.hub import Hub


class Drone():
    def __init__(self, name: str, node: Hub):
        self.__name = name
        self.__node = node
        self.__came_from = [node]
        self.__coordinates = node.xy
        self.__route = None
        self.__moving = False

    def __repr__(self):
        return self.__name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def node(self) -> Hub:
        return self.__node

    @node.setter
    def node(self, new_node: Hub) -> None:
        if isinstance(new_node, Hub):
            self.__node = new_node
            self.coordinates = new_node.xy
        else:
            raise TypeError('invalid drone node type')

    @property
    def route(self) -> list[Hub]:
        return self.__route

    @route.setter
    def route(self, new_route: list[Hub]) -> None:
        if (isinstance(new_route, list)
                and all(isinstance(_, Hub) for _ in new_route)):
            self.__route = new_route
        else:
            raise TypeError('route must be a list of Hub objects')

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, new_coordinate: tuple[int, int]) -> None:
        if (len(new_coordinate) == 2 and isinstance(new_coordinate, tuple)
                and all(isinstance(_, int) for _ in new_coordinate)):
            self.__coordinates = new_coordinate
        else:
            raise TypeError('invalid drone coordinate type')

    def step(self, to: Hub) -> str:
        pass

    def _move(self, to: Hub) -> str:
        link = self.__node.links[f'{self.node}-{to}']
        link.use()
        self.__came_from.append(to)
        self.node.drones.remove(self)
        to.drones.append(self)
        self.node = to
        return f'{self.name}-{to} '

    def _wait(self) -> None:
        return ''
