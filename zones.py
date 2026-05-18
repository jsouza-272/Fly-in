"""Zone definitions used to classify hubs on the map."""

from enum import Enum


class Zone(Enum):
    """Supported zone types for hubs on the map."""

    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
