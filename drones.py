from mapbuilder.hub import Hub


class Drones():
    def __init__(self, name: str, node: Hub):
        self.name = name
        self.node = node
        self.came_from = [node]

    def __repr__(self):
        return self.name

    def move(self, to: Hub) -> str:
        if not to.free() or self.node == to or to in self.came_from:
            return ''
        self.came_from.append(to)
        self.node.drones.remove(self)
        to.drones.append(self)
        self.node = to
        return f'{self.name}-{to} '
