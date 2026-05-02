from map.hub import Hub


class Drone():
    def __init__(self, name: str, node: Hub | None):
        self.__name = name
        self.__coordinates = None
        self.__node = node
        self.__route = []
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
        elif not new_node and self.__moving:
            self.__node = new_node
            self.coordinates = None
        else:
            raise TypeError('invalid drone node type')

    @property
    def route(self) -> list[Hub]:
        return self.__route

    @route.setter
    def route(self, new_route: list[Hub]) -> None:
        if (isinstance(new_route, list)
                and all(isinstance(_, Hub) for _ in new_route)):
            if self.node and self.node in new_route:
                self.__route = new_route[:new_route.index(self.node)]
            else:
                raise ValueError('Invalid route')
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
        elif not self.coordinates and self.__moving:
            self.__coordinates = None
        else:
            raise TypeError('invalid drone coordinate type')

    @property
    def moving(self) -> bool:
        return self.__moving

    def walk(self) -> str:
        if not self.route:
            return ''
        goal = self.route[-1]
        link = goal.links[f'{goal}-{self.node}']
        if goal.blocked:
            raise ValueError('PANIC')
        if self.__moving:
            self.node = goal
            goal.drones.append(self)
            self.__moving = False
            return f'{self}-{goal}'
        elif goal.restricted and goal.free() and link.can_use():
            self.node.drones.remove(self)
            link.use()
            self.__moving = True
            self.node = None
            return f'{link}'
        elif goal.free() and link.can_use():
            goal.drones.append(self)
            link.use()
            self.node.drones.remove(self)
            self.route.pop()
            return f'{self}-{goal}'
