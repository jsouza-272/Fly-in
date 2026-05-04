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
    def node(self, new_node: Hub | None) -> None:
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

    def move(self, to: Hub) -> str:
        link = self.node.links.get((self.node, to))
        msg = f'{self}-wait'
        if (not isinstance(to, Hub) or not link or to not in self.route
            or to.blocked):
            raise TypeError(f'invalid, {to} {link} {self.node} {self.route} {self.node.links}')
        if to.free() and link.can_use():
            if to.restricted and not to.reserved and not self.moving:
                to.reserved
                self.node.drones.remove(self)
                link.use()
                self.__moving = True
                self.node = None
            elif self.moving:
                to.reserved = False
                self.__moving = False
                self.node = to
                to.drones.append(self)
                msg = f'{self}-{to} '
            elif not to.restricted:
                self.node.drones.remove(self)
                link.use()
                to.drones.append(self)
                self.node = to
                msg = f'{self}-{to} '
        return msg, 
