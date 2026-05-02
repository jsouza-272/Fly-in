from map.hub import Hub
from map.map import Map
from abc import ABC, abstractmethod


class Algorithm(ABC):
    @abstractmethod
    def algorithm(self, graph: Map, rejected: list[Hub] = []) -> list[Hub]:
        pass
