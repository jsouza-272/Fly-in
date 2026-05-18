"""Visual interpolation utilities for drone movement rendering."""

from drones import Drone
from pygame import Vector2


class VisualDrone():
    """Represents the interpolated visual state of a drone."""

    def __init__(self, drone: Drone):
        """Initializes the drone visual position and animation speed."""
        self.pos = Vector2(drone.coordinates)
        self.speed = 0.1

    def update(self, to: Vector2) -> None:
        """Moves the visual position toward the target."""
        if (self.pos - to).length() < self.speed:
            self.pos = to
        else:
            self.pos += (to - self.pos).normalize() * self.speed
