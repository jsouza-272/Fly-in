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
        self.drones = []
        self.links = []
        if metadata:
            self.set_metadata(metadata)
        self.blocked = True if self.zone == Zone.BLOCKED else False
        self.set_cost()

    def __repr__(self):
        return self.name

    def set_metadata(self, metadata: dict) -> None:
        for key, value in metadata.items():
            if key == 'color':
                for c in Colors:
                    if c.value == value:
                        self.color = c
                        break
            elif key == 'zone':
                for z in Zone:
                    if z.value == value:
                        self.zone = z
                        break
            else:
                self.max_drones = value

    def set_link_capacity(self, max_link_capacity: int = 1) -> None:
        self.max_link_capacity = max_link_capacity

    def set_cost(self) -> None:
        if self.zone == Zone.BLOCKED:
            self.cost = 999
        elif self.zone == Zone.PRIORITY:
            self.cost = -1
        elif self.zone == Zone.RESTRICTED:
            self.cost = 10
        else:
            self.cost = 1

    def free(self) -> bool:
        return len(self.drones) < self.max_drones
