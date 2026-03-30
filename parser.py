from enum import Enum


class Colors(Enum):
    GREEN = 'green'
    RED = 'red'
    PURPLE = 'purple'
    BROWN = 'brown'
    ORANGE = 'orange'
    MAROON = 'maroon'
    GOLD = 'gold'
    BLACK = 'black'
    DARKRED = 'darkred'
    VIOLET = 'violet'
    CRIMSON = 'crimson'
    RAINBOW = 'rainbow'
    BLUE = 'blue'
    YELLOW = 'yellow'
    CYAN = 'cyan'
    LIME = 'lime'
    MAGENTA = 'magenta'


class Parser():
    @staticmethod
    def parsing(map_file: str):
        result = {'connection': [],
                  'hub': []}
        with open(map_file) as map:
            for line in map.readlines():
                line = line.replace('\n', '').replace(':', '')
                if not line.startswith('#') and line:
                    args = line.split(maxsplit=4)
                    if 'nb_drones' in args:
                        result[args[0]] = args[1]
                    elif 'connection' in args:
                        result[args[0]].append(args[1])
                    elif 'hub' in args:
                        result[args[0]].append([args[1],
                                                int(args[2]),
                                                int(args[3]),
                                                args[4]])
                    else:
                        new = {args[0]: [args[1], int(args[2]),
                                         int(args[3]), args[4]]}
                        result.update(new)

        return result


result = Parser.parsing('maps/challenger/01_the_impossible_dream.txt')
print(result)
