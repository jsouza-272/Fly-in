from enum import Enum


class Zone(Enum):
    """Supported zone types for hubs on the map."""

    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
