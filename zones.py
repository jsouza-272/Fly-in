from enum import Enum


class Zone(Enum):
    """Tipos de zona suportados para hubs no mapa."""

    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
