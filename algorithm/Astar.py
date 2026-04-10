from mapbuilder.hub import Hub
from mapbuilder import MapBuilder
import math


class Astar():
    def __init__(self):
        pass

    def euclidean(self, current: tuple[int, int],
                  goal: tuple[int, int]) -> int:
        cx, cy = current
        gx, gy = goal
        return int(math.sqrt((gx - cx)**2 + (gy - cy)**2))

    def algorithm(self, graph: MapBuilder) -> None:
        map = graph.map
        open_set = {map[0]}
        close_set = set()
        gscore = {map[0]: 0}
        fscore = {map[0]: 0 + self.euclidean(map[0].xy,
                                             map[1].xy)}
        camefrom = {}

        while open_set:
            currend_node = min(fscore, key=lambda k: fscore[k])
            neighbors = [n for n in currend_node.neighbors
                         if n not in close_set]
            for n in neighbors:
                if n not in open_set:
                    open_set.add(n)
                    gscore[n] = gscore[currend_node] + n.cost
                    fscore[n] = gscore[n] + self.euclidean(n.xy, map[1].xy)
                    camefrom[n] = currend_node

                elif n in gscore and gscore[currend_node] + n.cost < gscore[n]:
                    gscore[n] = gscore[currend_node] + n.cost
                    fscore[n] = gscore[n] + self.euclidean(n.xy, map[1].xy)
                    camefrom[n] = currend_node

            open_set.discard(currend_node)
            close_set.add(currend_node)
            fscore.pop(currend_node)
            if currend_node == map[1]:
                break
        return self.make_path(camefrom, map[1], map[0])

    def make_path(self, camefrom: dict, goal: Hub, start: Hub):
        path = [goal]
        current = goal
        while True:
            path.append(camefrom[current])
            current = camefrom[current]
            if current == start:
                break
        return path
        
