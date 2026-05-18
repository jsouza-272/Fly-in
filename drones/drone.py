"""Drone domain model and movement state transitions."""

from map import Hub
from map import Link


class Drone():
    """Represents a drone and its movement state on the map."""

    def __init__(self, name: str, node: Hub | None):
        """Initializes name, starting position, and movement state."""
        self.__name = name
        self.__coordinates = node.xy if node else (0, 0)
        self.__node = node
        self.__old_node: Hub | None = None
        self.__moving = False

    def __repr__(self) -> str:
        """Returns the string representation of the drone."""
        return self.__name

    @property
    def name(self) -> str:
        """Returns the drone name."""
        return self.__name

    @property
    def old_node(self) -> Hub | None:
        """Returns the previous known hub before movement."""
        return self.__old_node

    @property
    def node(self) -> Hub | None:
        """Returns the drone current hub, if available."""
        return self.__node

    @node.setter
    def node(self, new_node: Hub) -> None:
        """Updates current hub and adjusts coordinates based on state."""
        if isinstance(new_node, Hub) and not self.__moving:
            self.__node = new_node
            self.coordinates = new_node.xy
        elif isinstance(new_node, Hub) and self.__moving and self.__node:
            new_x = (self.__node.xy[0] + new_node.xy[0]) / 2
            new_y = (self.__node.xy[1] + new_node.xy[1]) / 2
            self.coordinates = (new_x, new_y)
            self.__node = None
        else:
            raise TypeError('invalid drone node type')

    @property
    def coordinates(self) -> tuple[float, float]:
        """Returns the current coordinates of the drone."""
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, new_coordinate: tuple[float, float]) -> None:
        """Updates drone coordinates after type validation."""
        if (len(new_coordinate) == 2 and isinstance(new_coordinate, tuple)
                and all(isinstance(_, (int, float)) for _ in new_coordinate)):
            self.__coordinates = new_coordinate
        else:
            raise TypeError('invalid drone coordinate type')

    @property
    def moving(self) -> bool:
        """Indicates whether the drone is moving between hubs."""
        return self.__moving

    def move(self, to_node: Hub, link_to_use: Link | None) -> str:
        """Attempts to move the drone to the destination hub."""
        msg = ''
        if not isinstance(to_node, Hub):
            raise TypeError('invalid node \"to_node\"', to_node)
        if not link_to_use and not self.__moving:
            raise TypeError(self, 'Link not exist', self.node, to_node)
        if to_node.blocked:
            raise TypeError('PANIC')
        if self.moving:
            to_node.reserved = False
            self.__moving = False
            self.node = to_node
            to_node.drones.append(self)
            msg = f'{self}-{to_node} '
        elif (to_node.restricted and link_to_use and
              (link_to_use.can_use() or to_node.free())):
            if not to_node.reserved and not self.moving and self.node:
                to_node.reserved = True
                self.node.drones.remove(self)
                if link_to_use:
                    link_to_use.use()
                self.__moving = True
                self.__old_node = self.node
                self.node = to_node
        elif to_node.free() and link_to_use and link_to_use.can_use():
            if not to_node.restricted and self.node:
                self.node.drones.remove(self)
                if link_to_use:
                    link_to_use.use()
                to_node.drones.append(self)
                self.node = to_node
                msg = f'{self}-{to_node} '
        return msg
