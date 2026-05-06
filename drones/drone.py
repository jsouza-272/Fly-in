from map import Hub
from map import Link
from errors import DroneRunningError


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
            if self.node and not self.moving and self.node in new_route:
                self.__route = new_route[:new_route.index(self.node)]
            elif not self.node and self.moving:
                raise DroneRunningError("cant change route")
            else:
                raise ValueError('Invalid route')
        else:
            raise TypeError('route must be a list of Hub objects')

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, new_coordinate: tuple[int, int]) -> None:
        if self.__moving:
            self.__coordinates = None
        elif (len(new_coordinate) == 2 and isinstance(new_coordinate, tuple)
                and all(isinstance(_, int) for _ in new_coordinate)):
            self.__coordinates = new_coordinate
        else:
            raise TypeError('invalid drone coordinate type')

    @property
    def moving(self) -> bool:
        return self.__moving

    def move(self, to_node: Hub, link_to_use: Link) -> tuple[str, None | Hub]:
        msg = f'{self}-wait '
        node_to_remove = None
        if not isinstance(to_node, Hub):
            raise TypeError('invalid node \"to_node\"', to_node)
        if not link_to_use and not self.__moving:
            raise TypeError(self, 'Link not exist', self.node, to_node)
        if to_node not in self.route:
            raise TypeError(to_node, 'not in route')
        if to_node.blocked:
            raise TypeError('PANIC')
        # if self.moving:
        #     print(self.node, to_node, link_to_use)
        if to_node.free() and link_to_use.can_use():
            if (to_node.restricted and not to_node.reserved
                    and not self.moving):
                msg = f'{self}-moving '
                to_node.reserved = True
                self.node.drones.remove(self)
                link_to_use.use()
                self.__moving = True
                self.node = None
            elif not to_node.restricted:
                self.node.drones.remove(self)
                link_to_use.use()
                to_node.drones.append(self)
                node_to_remove = to_node
                self.node = to_node
                msg = f'{self}-{to_node} '
        elif self.moving:
                to_node.reserved = False
                self.__moving = False
                node_to_remove = to_node
                self.node = to_node
                to_node.drones.append(self)
                msg = f'{self}-{to_node} '
                # print(node_to_remove, to_node)
        return msg, node_to_remove
