"""Hub domain model with capacity, metadata, and link management."""

from __future__ import annotations
from zones import Zone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .map import Link
    from drones import Drone


class Hub():
    """Represents a hub with metadata, links, and resident drones."""

    def __init__(self, name: str, x: int,
                 y: int, metadata: dict | None = None,
                 nb_drones: int | None = None):
        """Initializes basic hub data and applies optional metadata."""
        self.name = name
        self.xy = (float(x), float(y))
        self.color = None
        self.zone = Zone.NORMAL
        self.max_drones = 1
        self.drones: list['Drone'] = []
        self.links: dict[tuple, 'Link'] = {}
        self.__reserved = False
        if metadata:
            self.set_metadata(metadata, nb_drones)
        self.blocked = True if self.zone == Zone.BLOCKED else False
        self.restricted = True if self.zone == Zone.RESTRICTED else False
        self.set_cost()

    def __repr__(self) -> str:
        """Returns the hub name as its string representation."""
        return self.name

    @property
    def reserved(self) -> bool:
        """Indicates whether the hub is reserved by a moving drone."""
        return self.__reserved

    @reserved.setter
    def reserved(self, reserve: bool) -> None:
        """Updates reservation state with consistency checks."""
        if self.__reserved and reserve:
            raise ValueError('fail')
        elif not reserve and not self.__reserved:
            raise ValueError("fail")
        else:
            self.__reserved = reserve

    def set_metadata(self, metadata: dict,
                     nb_drones: int | None) -> None:
        """Applies color, zone, and capacity metadata to the hub."""
        if not metadata.get('max_drones') and nb_drones:
            self.max_drones = nb_drones
        for key, value in metadata.items():
            if key == 'color':
                self.color = value
            elif key == 'zone':
                self.zone = Zone(value)
            else:
                self.max_drones = value

    def set_cost(self) -> None:
        """Sets traversal cost according to hub zone."""
        if self.zone == Zone.BLOCKED:
            self.cost = 99999
        elif self.zone == Zone.RESTRICTED:
            self.cost = 2
        elif self.zone == Zone.PRIORITY:
            self.cost = 0
        else:
            self.cost = 1

    def get_link(self, next: 'Hub') -> Link | None:
        """Gets the link connecting this hub to the next one."""
        return self.links.get((self, next))

    def free(self) -> bool:
        """Reports whether the hub has capacity for more drones."""
        if self.__reserved:
            return len(self.drones) + 1 < self.max_drones
        else:
            return len(self.drones) < self.max_drones

    def reset_links(self) -> None:
        """Resets usage on all links connected to the hub."""
        for link in self.links.values():
            link.reset_usage()
