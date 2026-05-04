from zones import Zone
from colors import Colors
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .map import Link


class Hub():
    def __init__(self, name: str, x: int,
                 y: int, metadata: dict | None = None,
                 nb_drones: int | None = None):
        self.name = name
        self.xy = (x, y)
        self.color = None
        self.zone = Zone.NORMAL
        self.max_drones = 1
        self.drones = []
        self.links: dict[str, 'Link'] = {}
        self.__reserved = False
        if metadata:
            self.set_metadata(metadata, nb_drones)
        self.blocked = True if self.zone == Zone.BLOCKED else False
        self.restricted = True if self.zone == Zone.RESTRICTED else False
        self.set_cost()

    def __repr__(self) -> str:
        return self.name

    @property
    def reserved(self) -> bool:
        return self.__reserved

    @reserved.setter
    def reserved(self, reserve: bool) -> None:
        if self.__reserved and reserve:
            raise ValueError('fail')
        elif not reserve and not self.__reserved:
            raise ValueError("fail")
        else:
            self.__reserved = reserve

    def set_metadata(self, metadata: dict,
                     nb_drones: int | None) -> None:
        if not metadata.get('max_drones') and nb_drones:
            self.max_drones = nb_drones
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

    def set_cost(self) -> None:
        if self.zone == Zone.BLOCKED:
            self.cost = 999
        elif self.zone == Zone.PRIORITY:
            self.cost = -1
        elif self.zone == Zone.RESTRICTED:
            self.cost = 10
        else:
            self.cost = 1

    def get_link(self, next: 'Hub') -> 'Link':
        return self.links.get((self, next))

    def free(self) -> bool:
        if self.__reserved:
            return len(self.drones) + 1 < self.max_drones
        else:
            return len(self.drones) < self.max_drones

    def reset_links(self) -> None:
        for link in self.links:
            link.reset_usage()
