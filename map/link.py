from .hub import Hub
from typing import Any


class Link():
    def __init__(self, zone1: Hub, zone2: Hub,
                 metadata: dict[str, Any] | None = None) -> None:
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = 1
        self.usage = 0
        if metadata:
            self.set_metadata(metadata)

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        for key, value in metadata.items():
            if key == 'max_link_capacity':
                self.max_link_capacity = value

    def can_use(self) -> bool:
        return self.usage < self.max_link_capacity

    def use(self) -> None:
        self.usage += 1

    def get_current_hub(self, current: Hub) -> Hub | None:
        if self.zone1 == current:
            return self.zone1
        if self.zone2 == current:
            return self.zone2
        return

    def get_next_hub(self, current: Hub) -> Hub | None:
        if self.zone1 == current:
            return self.zone2
        if self.zone2 == current:
            return self.zone1

    def reset_usage(self) -> None:
        self.usage = 0
