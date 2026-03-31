class Hub():
    def __init__(self, name: str, x: int,
                 y: int, metadata: dict):
        self.name = name
        self.x = x
        self.y = y
        self.metadata = metadata
        self.neighbors = []

    def add_neighbor(self, neighbor: 'Hub') -> None:
        if neighbor not in self.neighbors and self not in neighbor.neighbors:
            self.neighbors.append(neighbor)
            neighbor.neighbors.append(self)

    def __repr__(self):
        return self.name
