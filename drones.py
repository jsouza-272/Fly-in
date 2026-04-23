from map.hub import Hub


class Drones():
    def __init__(self, name: str, node: Hub):
        self.__name = name
        self.__node = node
        self.__came_from = [node]
        self.__destination = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def node(self) -> Hub:
        return self.__node

    @property
    def destination(self) -> list[Hub]:
        return self.__destination

    @destination.setter
    def destination(self, new_path: list[Hub]) -> None:
        if (isinstance(new_path, list)
                and all([isinstance(_, Hub) for _ in new_path])):
            self.__destination = new_path[new_path.index(self.__node):]
        else:
            raise TypeError('Incompatible type')

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.__node.xy

    def __repr__(self):
        return self.__name

    def set_destination(self, path: list[Hub]) -> None:
        self.__destination = path

    def step(self) -> str:
        if isinstance(self.__destination, list) and self.__destination:
            step = self.__destination.pop()
            if step.free():
                return self.move(step)

    def move(self, to: Hub) -> str:
        link = self.__node.get_link(to)
        if link and link.can_use():
            self.__destination.pop()
            link.use()
            self.__came_from.append(to)
            self.node.drones.remove(self)
            to.drones.append(self)
            self.node = to
            return f'{self.__name}-{to} '
        return ''

    def wait(self) -> None:
        return
