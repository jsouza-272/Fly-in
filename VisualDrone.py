from drones import Drone
from pygame import Vector2


class VisualDrone():
    def __init__(self, drone: Drone):
        self.pos = Vector2(drone.coordinates)
        self.speed = 0.1

    def update(self, to: Vector2) -> None:
        if (self.pos - to).length() < self.speed:
            self.pos = to
        else:
            self.pos += (to - self.pos).normalize() * self.speed
