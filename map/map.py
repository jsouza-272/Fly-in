from .hub import Hub
from .link import Link


class Map():
    def __init__(self, nb_drones: int, connections: list[dict],
                 start_hub: dict, end_hub: dict, hub: list[dict] = []):
        self.map = self.build_map(hub, start_hub, end_hub,
                                  connections, nb_drones)
        self.__start_hub = self.map[0]
        self.__end_hub = self.map[1]

    @property
    def start_hub(self) -> Hub:
        return self.__start_hub

    @property
    def end_hub(self) -> Hub:
        return self.__end_hub

    def build_map(self, hub: list[dict], start_hub: dict,
                  end_hub: dict, connections: list[dict],
                  nb_drones: int) -> list[Hub]:
        map = [Hub(**start_hub, nb_drones=nb_drones),
               Hub(**end_hub, nb_drones=nb_drones)]
        map.extend([Hub(**h) for h in hub])
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
                node1.links.update({(node1, node2): link})
                node2.links.update({(node2, node1): link})
        return map

    def reset_links(self) -> None:
        for hub in self.map:
            hub.reset_links()
