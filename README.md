*This project has been created as part of the 42 curriculum by Jsouza*

# Fly-in

## Description

Fly-in is a drone-routing simulation built in Python. Given a map file describing hubs, connections, and zone constraints, it finds the optimal weighted path from a start hub to an end hub and simulates a fleet of drones moving through that network under turn and capacity constraints.

## Features

- **Map parser** — validates `.txt` map files with hubs, connections, zones (`normal`, `blocked`, `restricted`, `priority`), colors, and capacity constraints.
- **Dijkstra pathfinding** — computes the lowest-cost weighted route through the hub graph while excluding blocked zones and accounting for restricted-zone movement cost.
- **Simulation engine** — steps the drone fleet turn by turn, respecting per-link and per-hub capacity limits.
- **Pygame GUI** — renders the map, route, and drone positions interactively.

## Instructions

### Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (installed automatically by `make install`)

### Installation

```bash
make install
```

This creates a `.venv` virtual environment and installs all dependencies via `uv sync`.

### Execution

```bash
python3 fly_in.py <map_path.txt>
# or using make (defaults to maps/challenger/01_the_impossible_dream.txt)
make run
# run a specific map via make
make run MAP=maps/easy/01_linear_path.txt
# step through all built-in maps for visual testing
python3 fly_in.py --debug
```

### Linting

```bash
make lint   # runs flake8 + mypy
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

## Algorithm and Implementation Strategy

The implementation follows a layered object-oriented design:

- **Parsing/validation layer**: `parser.py` validates format, constraints, metadata, uniqueness rules, and raises explicit parsing errors for invalid maps.
- **Graph/model layer**: `map/` and `zones.py` represent hubs, links, zone types, and movement-related properties.
- **Pathfinding layer**: `algorithm/dijkstra.py` computes a weighted route using destination-zone cost and reconstructs the final path via predecessor mapping.
- **Simulation layer**: `emulation.py` advances turns, applies movement decisions, enforces capacity limits, and records state snapshots for replay.

### How pathfinding works in this project

The route is computed with a Dijkstra-style search centered on hub costs:

1. Start from `start_hub` with accumulated cost `0`.
2. Keep two sets:
   - **open_set**: hubs to evaluate next.
   - **close_set** (closed set): already-evaluated hubs (plus any explicitly rejected hubs).
3. Repeatedly select the hub with the smallest known accumulated cost.
4. Expand its neighbors through existing links, skipping blocked or closed hubs.
5. For each valid neighbor, compute a new candidate cost (`current_cost + neighbor.cost`):
   - if the neighbor is new, record this cost and predecessor;
   - if it was seen before with a higher cost, update cost and predecessor.
6. Stop when `end_hub` is selected, then rebuild the path by walking predecessors backward from end to start.
7. If no route reaches the end hub, raise `CantSolveGraphError`.

Because costs are attached to hubs (not links), the algorithm naturally models zone penalties (such as restricted hubs) while still finding the lowest total route under map constraints.

This strategy separates responsibilities so input validation, routing, simulation, and rendering remain maintainable and testable.

## Visual Representation

The project provides a graphical simulation using Pygame (`Gui.py` and `VisualDrone.py`):

- It displays hubs, links, selected paths, and drone positions per turn.
- It reflects map semantics (including colors/zone information) to make route analysis clearer.
- It provides interactive playback controls (play/pause, next/previous turn, speed changes), which helps users understand scheduling choices and congestion behavior over time.

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

## Resources

- Python documentation: https://docs.python.org/3/
- Pygame documentation: https://www.pygame.org/docs/
- Dijkstra algorithm reference: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- Type hints and mypy documentation: https://mypy.readthedocs.io/

### AI Usage

AI was used as a support tool throughout this project. It helped clarify the project requirements, assisted with the graphical part when learning how to use Pygame, and supported debugging for some mypy and Makefile issues. It was also used to improve and organize parts of the documentation.

All AI-generated suggestions were reviewed, adapted, and validated before being kept in the project.
