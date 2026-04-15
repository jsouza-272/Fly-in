from map.hub import Hub


class Drones():
    def __init__(self, name: str, node: Hub):
        self.name = name
        self.node = node
        self.came_from = [node]
        self.destination = None

    def __repr__(self):
        return self.name

    def set_destination(self, path: list[Hub]) -> None:
        self.destination = path

    def step(self) -> None:
        if isinstance(self.destination, list) and self.destination:
            step = self.destination.pop()
            if step.free():
                self.move(step)

    def move(self, to: Hub) -> str:
        self.came_from.append(to)
        self.node.drones.remove(self)
        to.drones.append(self)
        self.node = to
        return f'{self.name}-{to} '
