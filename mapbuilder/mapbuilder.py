from .hub import Hub
from drones import Drones


class MapBuilder():
    def __init__(self, connections: list[dict], hub: list[dict],
                 nb_drones: int, start_hub: dict, end_hub: dict):
        self.connections = connections
        self.map = self.build_map(hub, start_hub, end_hub)
        self.drones = [Drones(f'D{i + 1}', self.map[0])
                       for i in range(nb_drones)]
        self.map[0].drones.extend(self.drones)

    def build_map(self, hub: list[dict], start_hub: dict, end_hub: dict):
        hubs = [start_hub, end_hub]
        hubs.extend(hub)
        map = [Hub(**h) for h in hubs]
        for connection in self.connections:
            node1 = None
            node2 = None
            for node in map:
                if node.name == connection['zone1']:
                    node1 = node
                if node.name == connection['zone2']:
                    node2 = node
            if node1 and node2:
                node1.add_neighbor(node2)
        return map
