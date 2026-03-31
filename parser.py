from enum import Enum
from errors import ParserError


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
        try:
            with open(map_file) as map:
                for line in map.readlines():
                    line = line.replace('\n', '').replace(':', '')
                    if not line.startswith('#') and line:
                        args = line.split(maxsplit=4)
                        if 'nb_drones' in args:
                            result[args[0]] = args[1]
                        elif 'connection' in args:
                            result[args[0]].append(tuple(args[1].split('-')))
                        elif 'hub' in args:
                            result[args[0]].append([int(arg) if arg.isdigit()
                                                   else arg
                                                   for arg in args[1:]])
                        else:
                            new = {args[0]: [int(arg) if arg.isdigit() else arg
                                             for arg in args[1:]]}
                            result.update(new)

            return result
        except FileNotFoundError as e:
            print(e)
        except Exception:
            raise ParserError('Error: invalid map format')

