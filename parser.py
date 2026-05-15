from errors import ParserError
from typing import Any
from pygame.color import THECOLORS


ZONES = {'normal', 'blocked', 'restricted', 'priority'}


class Parser():
    def __init__(self, map_path: str):
        res = map_path.split('.', maxsplit=1)
        if res[1] != 'txt':
            raise ParserError(f"Invalid file extension, got: \"{res[1]}\""
                                f", expected: \"txt\"")
        with open(map_path) as lines:
            self.lines = lines.read().splitlines()
        self.names = set()
        self.coordinates = set()

    def parsing(self):
        config = {}
        self.check_lines(self.lines)
        config.update(self.check_first_line(self.lines))
        config.update(self.check_start_hub(self.lines, config['nb_drones']))
        config.update(self.check_hub(self.lines))
        config.update(self.check_end_hub(self.lines, config['nb_drones']))
        config.update(self.check_conections(self.lines))
        return config

    def check_lines(self, lines: list[str]) -> None:
        valid = ('#', 'nb_drones', 'start_hub', 'hub', 'end_hub',
                 'connection')
        for line in lines:
            if line and not line.startswith(valid):
                raise ParserError(f'Line {self.find_line(line)}: invalid line')
            if line and not line.startswith('#') and '#' in line:
                lines[lines.index(line)] = line.split('#')[0]

    def check_first_line(self, lines: list[str]) -> dict[str, int]:
        for line in lines:
            if line and not line.startswith('#'):
                break
        if 'nb_drones' not in line:
            raise ParserError(f'Line {self.find_line(line)}: first line must \
be start with nb_drones: <positive_integer>')
        else:
            nb_drones_split = line.strip().split(':')
            try:
                nb_drones = {nb_drones_split[0]: int(nb_drones_split[1])}
                if nb_drones[nb_drones_split[0]] < 0:
                    raise ValueError()
                return nb_drones
            except ValueError:
                raise ParserError(f'Line {self.find_line(line)}: invalid \
value for nb_drones, expected a positive integer')

    def check_start_hub(self, lines: list[str], nb_drones: int) -> dict[str, Any]:
        ctrl = False
        start_hub = {'start_hub': {}}
        try:
            for line in lines:
                if line.startswith('start_hub'):
                    if ctrl:
                        raise ParserError(f'Line {self.find_line(line)}: too \
many start_hub')
                    else:
                        ctrl = True
                        if line.split()[1].isdigit():
                            raise ParserError(f'start_hub need name')
                        start_hub['start_hub'].update({'name':
                                                       self.check_hub_name(
                                                           line)})
                        start_hub['start_hub'].update({'x': int(line.
                                                                split()[2])})
                        start_hub['start_hub'].update({'y': int(line.
                                                                split()[3])})
                        self.check_coordinates(start_hub['start_hub']['x'],
                                               start_hub['start_hub']['x'])
                        try:
                            metadata = self.check_hub_metadata(
                                {'metadata': line.split(maxsplit=4)[4]})
                            if metadata['metadata'].get('zone') == 'blocked':
                                raise ParserError('Start zone cannot '
                                                  'be blocked')
                            max_drones = metadata['metadata'].get('max_drones')
                            if max_drones and max_drones < nb_drones:
                                raise ParserError('The max_drones value for start_hub'
                                                  ' cannot be less than nb_drones')
                            start_hub['start_hub'].update(metadata)
                        except IndexError:
                            pass
            if not ctrl:
                raise ParserError('start_hub not found')
        except ValueError:
            raise ParserError(f'Line {self.find_line(line)}: \
invalid coordnates')
        except (IndexError, KeyError):
            raise ParserError(f'Line {self.find_line(line)}: \
missing informations')
        except ParserError as e:
            raise ParserError(f'Line {self.find_line(line)}: {e}')
        return start_hub

    def check_end_hub(self, lines: list[str], nb_drones: int) -> dict[str, Any]:
        ctrl = False
        end_hub = {'end_hub': {}}
        try:
            for line in lines:
                if line.startswith('end_hub'):
                    if ctrl:
                        raise ParserError(f'Line {self.find_line(line)}: too \
many end_hub')
                    else:
                        ctrl = True
                        if line.split()[1].isdigit():
                            raise ParserError(f'end_hub need name')
                        end_hub['end_hub'].update({'name':
                                                   self.check_hub_name(line)})
                        end_hub['end_hub'].update({'x': int(
                            line.split()[2])})
                        end_hub['end_hub'].update({'y': int(
                            line.split()[3])})
                        self.check_coordinates(end_hub['end_hub']['x'],
                                               end_hub['end_hub']['y'])
                        try:
                            metadata = self.check_hub_metadata(
                                {'metadata': line.split(maxsplit=4)[4]})
                            if metadata['metadata'].get('zone') == 'blocked':
                                raise ParserError('End zone cannot '
                                                  'be blocked')
                            max_drones = metadata['metadata'].get('max_drones')
                            if max_drones and max_drones < nb_drones:
                                raise ParserError('The max_drones value for end_hub'
                                                  ' cannot be less than nb_drones')
                            end_hub['end_hub'].update(metadata)
                        except IndexError:
                            pass
            if not ctrl:
                raise ParserError('end_hub not found')
        except ValueError:
            raise ParserError(f'Line {self.find_line(line)}: \
invalid coordnates')
        except IndexError:
            raise ParserError(f'Line {self.find_line(line)}: \
missing informations')
        except ParserError as e:
            raise ParserError(f'Line {self.find_line(line)}: {e}')
        return end_hub

    def check_hub(self, lines: list[str]) -> dict:
        hubs = {'hub': []}
        try:
            for line in lines:
                if line.startswith('hub:'):
                    hub = {}
                    if line.split()[1].isdigit():
                        raise ParserError(f'hub need name')
                    hub.update({'name':
                                self.check_hub_name(line)})
                    hub.update({'x': int(line.split()[2])})
                    hub.update({'y': int(line.split()[3])})
                    self.check_coordinates(hub['x'], hub['y'])
                    try:
                        hub.update(self.check_hub_metadata(
                            {'metadata': line.split(maxsplit=4)[4]}))
                    except IndexError:
                        pass
                    hubs['hub'].append(hub)
        except ValueError:
            raise ParserError(f'Line {self.find_line(line)}: \
invalid coordnates')
        except IndexError:
            raise ParserError(f'Line {self.find_line(line)}: \
missing informations')
        except ParserError as e:
            raise ParserError(f'Line {self.find_line(line)}: {e}')
        if hubs['hub']:
            return hubs
        return {}

    def check_hub_metadata(self, hub: dict[str, Any]) -> dict[str, Any]:
        metadata = hub.get('metadata')
        if not metadata:
            return
        if any(_ not in metadata for _ in '[=]'):
            raise ParserError("invalid syntax use [<metadata_type>=<value>] \
for metadata")
        dup = {metadata.count(_) > 1: _[:-1]
               for _ in ('color=', 'zone=', 'max_drones=')}
        if any(dup):
            raise ParserError(f'Duplicate metadata field "{dup[True]}"')
        split_metadata = metadata.replace('[', '').replace(']', '').split()
        meta = {}
        try:
            for m in split_metadata:
                split_m = m.split('=')
                if not split_m[1]:
                    raise IndexError()
                if split_m[0] in ('color', 'max_drones', 'zone'):
                    if (split_m[1] in ZONES or split_m[1]
                        in THECOLORS or (split_m[0] == 'max_drones'
                                         and int(split_m[1]) > 0)):

                        meta[split_m[0]] = (int(split_m[1])
                                            if split_m[0] == 'max_drones'
                                            else split_m[1])
                    else:
                        if (split_m[0] == 'zone' and split_m[1] not in
                                ZONES):
                            raise ParserError("Invalid zone. Valid zones "
                                              "are: ", ZONES)
                        if (split_m[0] == 'color' and split_m[1] not in
                                THECOLORS):
                            raise ParserError(f"Invalid color: '{split_m[1]}' "
                                              "not exist")
                        if split_m[0] == 'max_drones' and int(split_m[1]) < 1:
                            raise ParserError('Invalid max_drones: value '
                                              'must be greater than 0')
                else:
                    raise ParserError(f'Invalid metadata "{split_m[0]}"')
        except IndexError:
            raise ParserError("Invalid format. \
Expected [<metadata_type>=<value>]")
        except ValueError:
            raise ParserError("max_drones must be a valid integer")
        return {'metadata': meta}

    def check_hub_name(self, line: str) -> str:
        split_line = line.split()[1:]
        for _ in split_line:
            if _.isdigit():
                split_line = split_line[0:split_line.index(_)]
                break
        if len(split_line) > 1 or '-' in split_line[0]:
            raise ParserError(f'Invalid name')
        if split_line[0] in self.names:
            raise ParserError(f'duplicate name "{split_line[0]}"')
        self.names.add(split_line[0])
        return split_line[0]

    def check_conections(self, lines: list[str]) -> dict[str, list]:
        connections = {'connections': []}
        crtl_list = []
        for line in lines:
            connection = {}
            if line.startswith('connection:'):
                splited_line = line.split()
                if len(splited_line) < 2:
                    raise ParserError(f'Line {self.find_line(line)}: invalid \
connection format. Expectd: connection: <zona1>-<zona2> [metadata]')
                zones = splited_line[1].split('-')
                if len(zones) != 2:
                    raise ParserError(f'Line {self.find_line(line)}: invalid \
connection format. Expectd: connection: <zona1>-<zona2> [metadata]')
                if zones[0] not in self.names or zones[1] not in self.names:
                    raise ParserError(f'Line {self.find_line(line)}: \
invalid zone name \"{zones[0] if zones[0] not in self.names else zones[1]}\"')
                if (tuple(zones) in crtl_list
                        or tuple(reversed(zones)) in crtl_list):
                    raise ParserError(f'Line {self.find_line(line)}: \
duplicate conection')
                if zones[0] == zones[1]:
                    raise ParserError(f'Line {self.find_line(line)}: Invalid \
zones both zones must be different')
                crtl_list.append(tuple(zones))
                connection['zone1'] = zones[0]
                connection['zone2'] = zones[1]
                try:
                    connection['metadata'] = self.check_connection_metadata(
                        line.split(maxsplit=2)[2])
                except ParserError as e:
                    raise ParserError(f'Line {self.find_line(line)}: {e}')
                except ValueError:
                    raise ParserError(f'Line {self.find_line(line)}: \
max_link_capacity must be a valid integer')
                except IndexError:
                    pass
                connections['connections'].append(connection)
        if not connections['connections']:
            raise ParserError('ERROR: connections required')
        return connections

    def check_connection_metadata(self, metadata: str) -> dict[str, Any]:
        if any(_ not in metadata for _ in '[=]'):
            raise ParserError('invalid syntax use [<metadata_type>=<value>] \
for metadata')
        dup = {metadata.count('max_link_capacity=') > 1: 'max_link_capacity'}
        if True in dup:
            raise ParserError(f'Duplicate metadata field "{dup[True]}"')
        metadata = metadata.strip('[]').split('=')
        if metadata[0] != 'max_link_capacity':
            raise ParserError('invalid metadata')
        if int(metadata[1]) < 1:
            raise ParserError('max_link_capacity value \
must be greater than 0')
        return {metadata[0]: int(metadata[1])}

    def check_coordinates(self, x: int, y: int) -> None:
        if (x, y) in self.coordinates:
            raise ParserError("Coordinates already exist")
        self.coordinates.add((x, y))

    def find_line(self, line: str) -> int:
        return self.lines.index(line) + 1
