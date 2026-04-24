from map.hub import Hub


class Drone():
    def __init__(self, name: str, node: Hub):
        self.__name = name
        self.__node = node
        self.__came_from = [node]
        self.__route = None
        self.__waiting = False

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
        return self.__node.xy

    def step(self, to: Hub) -> str:
        if isinstance(self.__route, list) and self.__route:
            step = self.__route[-1]
            if step.restricted and not self.__waiting:
                self.__waiting = True
                return self._wait()
            if (step.free() and step.get_link(to)
                    and step.get_link(to).can_use()):
                self.__waiting = False
                self.__route.pop()
                return self._move(step)
            else:
                return self._wait()

    def _move(self, to: Hub) -> str:
        link = self.__node.get_link(to)
        link.use()
        self.__came_from.append(to)
        self.node.drones.remove(self)
        to.drones.append(self)
        self.node = to
        return f'{self.__name}-{to} '

    def _wait(self) -> None:
        return ''
