from drones import Drone
from pygame import Vector2


class VisualDrone():
    def __init__(self, drone: Drone):
        self.pos = Vector2(drone.coordinates)

    def update(self, to: Vector2) -> None:
        if (self.pos - to).length() < 0.1:
            self.pos = to
        else:
            self.pos += (to - self.pos).normalize() * 0.03
