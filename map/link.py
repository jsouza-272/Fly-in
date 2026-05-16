from .hub import Hub
from typing import Any


class Link():
    """Represents a bidirectional connection between two hubs."""

    def __init__(self, zone1: Hub, zone2: Hub,
                 metadata: dict[str, Any] | None = None) -> None:
        """Initializes connected hubs and default link capacity."""
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = 1
        self.usage = 0
        if metadata:
            self.set_metadata(metadata)

    def __repr__(self) -> str:
        """Returns a string representation of the hub connection."""
        return f"{self.zone1}<->{self.zone2}"

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Applies supported metadata to the link."""
        for key, value in metadata.items():
            if key == 'max_link_capacity':
                self.max_link_capacity = value

    def can_use(self) -> bool:
        """Returns whether the link still has available capacity."""
        return self.usage < self.max_link_capacity

    def use(self) -> None:
        """Registers one link usage in the current turn."""
        self.usage += 1

    def get_current_hub(self, current: Hub) -> Hub | None:
        """Returns the current hub when it belongs to this link."""
        if self.zone1 == current:
            return self.zone1
        if self.zone2 == current:
            return self.zone2
        return None

    def get_next_hub(self, current: Hub) -> Hub | None:
        """Returns the opposite hub for the provided one on this link."""
        if self.zone1 == current:
            return self.zone2
        if self.zone2 == current:
            return self.zone1
        return None

    def reset_usage(self) -> None:
        """Resets the link usage counter."""
        self.usage = 0
