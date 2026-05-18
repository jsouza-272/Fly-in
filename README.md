*This project has been created as part of the 42 curriculum by Joao Souza*

# Fly-in

Fly-in is a drone-routing simulation built in Python. Given a map file describing hubs, connections, and zone constraints, it finds the optimal path from a start hub to an end hub using Dijkstra's algorithm, then animates a fleet of drones travelling that route in a Pygame GUI.

## Features

- **Map parser** — validates `.txt` map files with hubs, connections, zones (`normal`, `blocked`, `restricted`, `priority`), colors, and capacity constraints.
- **Dijkstra pathfinding** — computes the lowest-cost route through the hub graph while respecting blocked and restricted zones.
- **Simulation engine** — steps the drone fleet turn by turn, respecting per-link and per-hub capacity limits.
- **Pygame GUI** — renders the map, route, and drone positions interactively.

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (installed automatically by `make install`)

## Installation

```bash
make install
```

This creates a `.venv` virtual environment and installs all dependencies via `uv sync`.

## Usage

```bash
python3 fly_in.py <map_path.txt>
# or using make (defaults to maps/challenger/01_the_impossible_dream.txt)
make run
# run a specific map via make
make run MAP=maps/easy/01_linear_path.txt
# step through all built-in maps for visual testing
python3 fly_in.py --debug
```

### Controls (GUI)

| Key | Action |
|-----|--------|
| `→` | Next turn |
| `←` | Previous turn |
| `Space` | Play / Pause |
| `s` | Speed up / slow down |
| `r` | Reload current map (only while paused) |
| `Esc` | Quit / return to map selector |
| `n` (debug) | Next map |
| `b` (debug) | Previous map |

## Map File Format

A map file is a plain `.txt` file. Lines starting with `#` are comments.

```
nb_drones: <positive_integer>
start_hub <name> <x> <y> [metadata]
hub: <name> <x> <y> [metadata]
end_hub <name> <x> <y> [metadata]
connection: <name1>-<name2> [metadata]
```

**Metadata** is written as space-separated `[key=value]` pairs. Supported keys:

| Key | Applies to | Description |
|-----|-----------|-------------|
| `zone` | hub | `normal` \| `blocked` \| `restricted` \| `priority` |
| `color` | hub | any Pygame color name, or `rainbow` |
| `max_drones` | hub | maximum drones allowed at the hub simultaneously |
| `max_link_capacity` | connection | maximum drones allowed on the link per turn |

Example:

```
nb_drones: 3
start_hub SOURCE 0 0
hub: A 1 0 [zone=priority] [color=green]
hub: B 1 1 [max_drones=2]
end_hub DEST 2 0
connection: SOURCE-A
connection: A-DEST [max_link_capacity=2]
connection: SOURCE-B
connection: B-DEST
```

## Project Structure

```
fly_in.py          # entry point
parser.py          # map file parser & validator
emulation.py       # turn-based simulation engine
Gui.py             # Pygame graphical interface
VisualDrone.py     # drone sprite rendering
map/               # Map, Hub, and Link models
drones/            # Drone and DronesManager models
algorithm/         # Dijkstra implementation
zones.py           # Zone enum
errors/            # custom exception types
```

## Linting

```bash
make lint   # runs flake8 + mypy
```
