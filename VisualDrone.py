from drones import Drone
from pygame import Vector2


class VisualDrone():
    """Representa o estado visual interpolado de um drone."""

    def __init__(self, drone: Drone):
        """Inicializa posição visual e velocidade de animação do drone."""
        self.pos = Vector2(drone.coordinates)
        self.speed = 0.1

    def update(self, to: Vector2) -> None:
        """Move a posição visual em direção ao alvo."""
        if (self.pos - to).length() < self.speed:
            self.pos = to
        else:
            self.pos += (to - self.pos).normalize() * self.speed
