from .hub import Hub
from typing import Any


class Link():
    """Representa uma ligação bidirecional entre dois hubs."""

    def __init__(self, zone1: Hub, zone2: Hub,
                 metadata: dict[str, Any] | None = None) -> None:
        """Inicializa hubs conectados e capacidade padrão do link."""
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = 1
        self.usage = 0
        if metadata:
            self.set_metadata(metadata)

    def __repr__(self) -> str:
        """Retorna representação textual da conexão entre hubs."""
        return f"{self.zone1}<->{self.zone2}"

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Aplica metadados suportados ao link."""
        for key, value in metadata.items():
            if key == 'max_link_capacity':
                self.max_link_capacity = value

    def can_use(self) -> bool:
        """Retorna se o link ainda possui capacidade disponível."""
        return self.usage < self.max_link_capacity

    def use(self) -> None:
        """Registra uma utilização do link no turno atual."""
        self.usage += 1

    def get_current_hub(self, current: Hub) -> Hub | None:
        """Retorna o hub atual quando ele pertence ao link."""
        if self.zone1 == current:
            return self.zone1
        if self.zone2 == current:
            return self.zone2
        return None

    def get_next_hub(self, current: Hub) -> Hub | None:
        """Retorna o hub oposto ao informado neste link."""
        if self.zone1 == current:
            return self.zone2
        if self.zone2 == current:
            return self.zone1
        return None

    def reset_usage(self) -> None:
        """Reseta contador de uso do link."""
        self.usage = 0
