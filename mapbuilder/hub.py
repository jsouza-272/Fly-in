from zones import Zone
from colors import Colors


class Hub():
    def __init__(self, name: str, x: int,
                 y: int, metadata: dict | None = None):
        self.name = name
        self.xy = (x, y)
        self.color = None
        self.zone = Zone.NORMAL
        self.max_drones = 1
        self.neighbors = []
        self.drones = []
        if metadata:
            self.set_metadata(metadata)
        self.set_cost()

    def add_neighbor(self, neighbor: 'Hub') -> None:
        if neighbor not in self.neighbors and self not in neighbor.neighbors:
            self.neighbors.append(neighbor)
            neighbor.neighbors.append(self)

    def set_metadata(self, metadata: dict) -> None:
        for key, value in metadata.items():
            if key == 'color':
                for c in Colors:
                    if c.value == value:
                        self.color == c
                    else:
                        pass
            elif key == 'zone':
                for z in Zone:
                    if z.value == value:
                        self.zone == z
                    else:
                        pass
            else:
                self.max_drones = value

    def set_cost(self) -> None:
        if self.zone == Zone.BLOCKED:
            self.cost = 99
        elif self.zone == Zone.PRIORITY:
            self.cost = -1
        elif self.zone == Zone.RESTRICTED:
            self.cost = 2
        else:
            self.cost = 1

    def __repr__(self):
        return self.name

    def free(self) -> bool:
        return len(self.drones) < self.max_drones
