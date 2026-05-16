from .hub import Hub
from .link import Link


class Map():
    """Agrupa hubs e conexões, expondo utilitários do grafo."""

    def __init__(self, nb_drones: int, connections: list[dict],
                 start_hub: dict, end_hub: dict, hub: list[dict] = []):
        """Constrói o mapa a partir da configuração de entrada."""
        self.map = self.build_map(hub, start_hub, end_hub,
                                  connections, nb_drones)
        self.__start_hub = self.map[0]
        self.__end_hub = self.map[1]

    @property
    def start_hub(self) -> Hub:
        """Retorna o hub inicial do mapa."""
        return self.__start_hub

    @property
    def end_hub(self) -> Hub:
        """Retorna o hub final do mapa."""
        return self.__end_hub

    @property
    def map_bounds(self) -> tuple[float, float, float, float]:
        """Calcula limites máximos e mínimos das coordenadas do mapa."""
        max_x = max(self.map, key=lambda hub: hub.xy[0]).xy[0]
        max_y = max(self.map, key=lambda hub: hub.xy[1]).xy[1]
        min_x = min(self.map, key=lambda hub: hub.xy[0]).xy[0]
        min_y = min(self.map, key=lambda hub: hub.xy[1]).xy[1]
        return (max_x, max_y, min_x, min_y)

    def build_map(self, hub: list[dict], start_hub: dict,
                  end_hub: dict, connections: list[dict],
                  nb_drones: int) -> list[Hub]:
        """Cria hubs e links do mapa a partir de dados de configuração."""
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
        """Reseta uso de links em todos os hubs do mapa."""
        for hub in self.map:
            hub.reset_links()
