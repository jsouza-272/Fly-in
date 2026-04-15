from .hub import Hub
from drones import Drones
from .link import Link


class Map():
    def __init__(self, nb_drones: int, connections: list[dict],
                 start_hub: dict, end_hub: dict, hub: list[dict] = []):
        self.map = self.build_map(hub, start_hub, end_hub, connections)
        self.drones = [Drones(f'D{i + 1}', self.map[0])
                       for i in range(nb_drones)]
        self.map[0].drones.extend(self.drones)

    def build_map(self, hub: list[dict], start_hub: dict,
                  end_hub: dict, connections: list[dict]):
        hubs = [start_hub, end_hub]
        hubs.extend(hub)
        map = [Hub(**h) for h in hubs]
        for connection in connections:
            node1 = None
            node2 = None
            for node in map:
                if node.name == connection['zone1']:
                    node1 = node
                if node.name == connection['zone2']:
                    node2 = node
            if node1 and node2:
                link = Link(node1, node2, connection.get('metadata'))
                node1.links.append(link)
                node2.links.append(link)
        return map

    def set_drone_destination(self, path: list[Hub]) -> None:
        for d in self.drones:
            d.set_destination(path)

    def turn(self) -> None:
        pass
