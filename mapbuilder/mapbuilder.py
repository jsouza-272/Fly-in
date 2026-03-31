from parser import Colors
from .hub import Hub


class MapBuilder():
    def __init__(self, connection: list[tuple], hub: list[list],
                 nb_drones: int, start_hub: list, end_hub: list):
        self.connections = connection
        self.nb_drones = nb_drones
        self.map = self.build_map(hub, start_hub, end_hub)

    def build_map(self, hub: list[list], start_hub: list, end_hub: list):
        map = []
        hubs = [start_hub, end_hub]
        hubs.extend(hub)
        for h in hubs:
            if len(h) == 4:
                h[-1] = h[-1].replace('[', '')
                h[-1] = h[-1].replace(']', '')
                temp = h[-1].split()
                metadata = {t.split('=')[0]: int(t.split('=')[1])
                            if t.split('=')[1].isdigit()
                            else t.split('=')[1] for t in temp}
                if metadata['color'] not in Colors:
                    raise ValueError()
                h[-1] = metadata
            map.append(Hub(*h))
        for connection in self.connections:
            node1 = None
            node2 = None
            for node in map:
                if node.name == connection[0]:
                    node1 = node
                if node.name == connection[1]:
                    node2 = node
            if node1 and node2:
                node1.add_neighbor(node2)
                # print(node1, node1.neighbors)
                # print(node2, node2.neighbors)
