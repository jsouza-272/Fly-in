from map.hub import Hub
from map.map import Map
from errors import CantSolveGraphError
from .algorithm import Algorithm
import math


class Astar(Algorithm):
    def algorithm(self, graph: Map, rejected: list[Hub] = [],
                  start_hub: Hub | None = None,
                  end_hub: Hub | None = None) -> list[Hub]:
        end_hub = graph.end_hub if not end_hub else end_hub
        start_hub = graph.start_hub if not start_hub else start_hub
        open_set = {start_hub}
        close_set = set(rejected)
        gscore = {start_hub: 0}
        fscore = {start_hub: 0 + self._euclidean(start_hub.xy, end_hub.xy)}
        camefrom = {}

        while open_set:
            currend_node = min(fscore, key=lambda k: fscore[k])
            neighbors = [n.get_next_hub(currend_node)
                         for n in currend_node.links.values()
                         if n.get_next_hub(currend_node) not in close_set]
            for n in neighbors:
                if n not in open_set and not n.blocked:
                    open_set.add(n)
                    gscore[n] = gscore[currend_node] + n.cost
                    fscore[n] = gscore[n] + self._euclidean(n.xy,
                                                            end_hub.xy)
                    camefrom[n] = currend_node

                elif n in gscore and gscore[currend_node] + n.cost < gscore[n]:
                    gscore[n] = gscore[currend_node] + n.cost
                    fscore[n] = gscore[n] + self._euclidean(n.xy, end_hub.xy)
                    camefrom[n] = currend_node

            open_set.discard(currend_node)
            close_set.add(currend_node)
            fscore.pop(currend_node)
            if currend_node == end_hub:
                return self._make_path(camefrom, end_hub,
                                       start_hub)
        raise CantSolveGraphError("Error: path not exist")

    @staticmethod
    def _euclidean(current: tuple[int, int],
                   goal: tuple[int, int]) -> int:
        cx, cy = current
        gx, gy = goal
        return int(math.sqrt((gx - cx)**2 + (gy - cy)**2))

    @staticmethod
    def _make_path(camefrom: dict, goal: Hub, start: Hub) -> list[Hub]:
        path = [goal]
        current = goal
        while True:
            path.append(camefrom[current])
            current = camefrom[current]
            if current == start:
                break
        return path
