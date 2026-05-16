from __future__ import annotations
from zones import Zone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .map import Link
    from drones import Drone


class Hub():
    """Representa um hub com metadados, links e drones presentes."""

    def __init__(self, name: str, x: int,
                 y: int, metadata: dict | None = None,
                 nb_drones: int | None = None):
        """Inicializa dados básicos do hub e aplica metadados opcionais."""
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
        """Retorna o nome do hub como representação textual."""
        return self.name

    @property
    def reserved(self) -> bool:
        """Indica se o hub está reservado por um drone em trânsito."""
        return self.__reserved

    @reserved.setter
    def reserved(self, reserve: bool) -> None:
        """Atualiza estado de reserva com validações de consistência."""
        if self.__reserved and reserve:
            raise ValueError('fail')
        elif not reserve and not self.__reserved:
            raise ValueError("fail")
        else:
            self.__reserved = reserve

    def set_metadata(self, metadata: dict,
                     nb_drones: int | None) -> None:
        """Aplica metadados de cor, zona e capacidade ao hub."""
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
        """Define o custo de travessia conforme a zona do hub."""
        if self.zone == Zone.BLOCKED:
            self.cost = 99999
        elif self.zone == Zone.RESTRICTED:
            self.cost = 2
        elif self.zone == Zone.PRIORITY:
            self.cost = 0
        else:
            self.cost = 1

    def get_link(self, next: 'Hub') -> Link | None:
        """Obtém o link que conecta este hub ao próximo."""
        return self.links.get((self, next))

    def free(self) -> bool:
        """Informa se o hub possui capacidade para mais drones."""
        if self.__reserved:
            return len(self.drones) + 1 < self.max_drones
        else:
            return len(self.drones) < self.max_drones

    def reset_links(self) -> None:
        """Reseta o uso de todos os links conectados ao hub."""
        for link in self.links.values():
            link.reset_usage()
