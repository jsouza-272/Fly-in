from .hub import Hub
from drones import Drones
from .link import Link
from errors import AstarError


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
            d.set_destination(path.copy())

    def reset_links(self) -> None:
        for hub in self.map:
            hub.reset_links()

    def turn(self) -> None:
        from algorithm.Astar import Astar
        turn = 0
        while self.drones:
            move_message = ''
            for d in self.drones:
                print(d, d.node, d.node.links, d.destination)
                step = d.destination[-1]
                if d.node == step:
                    d.destination.pop()
                    step = d.destination[-1]
                if step.free():
                    move_message += d.move(step)
                    d.destination.pop()
                elif not step.free() and len(d.node.links) > 1:
                    try:
                        #print('old', d.destination)
                        new_path = Astar().algorithm(self, [step])
                        #print('new', new_path)
                        if d.node in new_path:
                            d.destination = new_path[new_path.index(d.node):]
                            #print('new', d.destination)
                            step = d.destination[-1]
                            if d.node == step:
                                d.destination.pop()
                                step = d.destination[-1]
                                move_message += d.move(step)
                                d.destination.pop()
                            else:
                                move_message += d.move(step)
                                d.destination.pop()
                    except AstarError:
                        #print('\n\nfail\n')
                        pass
                else:
                    d.wait()
                    #move_message += f"{d} waiting "
                if not d.destination and d.node == self.map[1]:
                    self.drones.remove(d)
                    print(d, 'removed')
                # if d.name == 'D2':
                #    print(d, d.node)
            print(move_message)
            turn += 1
            self.reset_links()
        print()
        print(turn, 'turns')
