from map.hub import Hub
from map.map import Map
from abc import ABC, abstractmethod


class Algorithm(ABC):
    @abstractmethod
    def algorithm(self, graph: Map, rejected: list[Hub] = [],
                  start_hub: Hub | None = None,
                  end_hub: Hub | None = None) -> list[Hub]:
        pass
