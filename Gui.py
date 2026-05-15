import pygame
from pygame import Color
from pygame.font import Font
from map import Map, Hub, Link
from drones import Drone
from emulation import SimulationEngine
from VisualDrone import VisualDrone
import random


class Gui():
    def __init__(self, map: Map, title: str,
                 emulator: SimulationEngine,
                 w_h: tuple[int, int] = (-1, -1)):
        pygame.init()
        w, h = w_h
        if w == -1 and h == -1:
            self.width = pygame.display.Info().current_w
            self.height = pygame.display.Info().current_h
        else:
            self.width = w
            self.height = h
        self.map = map
        self.visual_drones: dict[Drone, VisualDrone] = {}
        self.emulator = emulator
        self.screen = self._start(title)
        self.clock = pygame.time.Clock()

    def _start(self, title: str) -> pygame.Surface:
        fullscreen = 0
        if (self.height == pygame.display.Info().current_h
                and self.width == pygame.display.Info().current_w):
            fullscreen = pygame.FULLSCREEN
        pygame.display.set_caption(title)
        return pygame.display.set_mode((self.width, self.height), fullscreen)

    def _calc_scale_and_offset(self, padding) -> tuple[float, tuple]:
        map_bounds = self.map.map_bounds
        scale = self._calc_scale(padding, map_bounds)
        offset = self._calc_offset(scale, map_bounds)
        return scale, offset

    def _calc_scale(self, padding: int,
                    map_bounds: tuple) -> float:
        max_x, max_y, min_x, min_y = map_bounds
        map_width = max_x - min_x
        map_height = max_y - min_y
        if not map_width:
            map_width = 1
        if not map_height:
            map_height = 1
        scale_x = (self.width - padding*2) / map_width
        scale_y = (self.height - padding*2) / map_height
        return min(scale_x, scale_y)

    def _calc_offset(self, scale: float,
                     map_bounds: tuple) -> tuple[float, float]:
        max_x, max_y, min_x, min_y = map_bounds
        map_center_x = (max_x + min_x) / 2
        map_center_y = (max_y + min_y) / 2
        screen_center_x = self.width / 2
        screen_center_y = self.height / 2
        offset_x = screen_center_x - (map_center_x * scale)
        offset_y = screen_center_y - (map_center_y * scale)
        return offset_x, offset_y

    def _render_links(self, links: list[Link], scale: float,
                      offset: tuple) -> None:
        off_x, off_y = offset
        size = int(3 * (scale * 0.01))
        for link in links:
            x1, y1 = link.zone1.xy
            x2, y2 = link.zone2.xy
            mx1 = (x1 * scale) + off_x
            mx2 = (x2 * scale) + off_x
            my1 = (y1 * scale) + off_y
            my2 = (y2 * scale) + off_y
            pygame.draw.line(self.screen, Color('black'),
                             (mx1, my1), (mx2, my2), size)

    def _render_hubs(self, hubs: list[Hub], scale: float,
                     offset: tuple, font: Font) -> None:
        off_x, off_y = offset
        hub_size = max(10, min(60, scale * 0.1))
        circle_size = int(hub_size)
        for hub in hubs:
            x, y = hub.xy
            mx = (x * scale) + off_x
            my = (y * scale) + off_y
            if hub.color == 'rainbow':
                pygame.draw.circle(self.screen,
                                   Color(random.choice(list(pygame.color.THECOLORS))),
                               (mx, my), circle_size)
            else:
                pygame.draw.circle(self.screen,
                               Color(hub.color),
                               (mx, my), circle_size)
            self.screen.blit(font.render(hub.name, True, Color('black')),
                             (mx + (circle_size * 0.2), my + circle_size))

    def _render_drones(self, drones: list[Drone],
                       scale: float, offset: float, font: Font) -> bool:
        can_do_next_turn = False
        off_x, off_y = offset
        for drone in drones:
            target = drone.coordinates
            visual_drone = self.visual_drones[drone.name]
            visual_drone.update(pygame.Vector2(target))
            x, y = visual_drone.pos
            mx = (x * scale) + off_x
            my = (y * scale) + off_y
            size = int(scale * 0.05)
            border = [(mx, my + size + 3), (mx + size + 3, my),
                      (mx, my - size - 3), (mx - size - 3, my)]
            points = [(mx, my + size), (mx + size, my),
                      (mx, my - size), (mx - size, my)]
            pygame.draw.polygon(self.screen, Color('gray30'),
                                border)
            pygame.draw.polygon(self.screen, Color('gray50'),
                                points)
            txt = font.render(drone.name, True,
                              Color("black"))
            self.screen.blit(txt, (mx - scale * 0.028,
                             my - scale * 0.02))
        if all([drone.coordinates == self.visual_drones[drone.name].pos
               for drone in drones]):
            can_do_next_turn = True
        return can_do_next_turn

    def _render_map(self, map_state: list[Hub], drones_state: list[Drone]) -> bool:
        scale, offset = self._calc_scale_and_offset(300)
        set_link = set([link for hub in map_state
                        for link in hub.links.values()])
        self._render_links(set_link, scale, offset)
        self._render_hubs(map_state, scale,
                          offset, Font(None, int(scale * 0.12)))
        can_do_next_turn = self._render_drones(drones_state, scale, offset,
                                               Font(None, int(scale * 0.07)))
        pygame.display.flip()
        return can_do_next_turn

    def loop(self):
        t = True
        can_do = False
        return_value = ''
        turn = self.emulator.turn()
        index = 0
        map_state, drones_state = turn[index]
        self.visual_drones = {drone.name: VisualDrone(drone)
                              for drone in drones_state}
        do_next_turn = False
        font = Font(None, 30)
        turn_counter = 0
        drone_speed = 0.1
        limit = len(turn)
        while t:
            self.clock.tick(30)
            self.screen.fill(Color('gray80'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    t = False
                    return_value = 'q'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if drone_speed == 0.1:
                            drone_speed = 0.5
                        else:
                            drone_speed = 0.1
                        for vd in self.visual_drones.values():
                            vd.speed = drone_speed
                    if event.key == pygame.K_n:
                        t = False
                        return_value = 'n'
                    if event.key == pygame.K_ESCAPE:
                        t = False
                        return_value = 'q'
                    if event.key == pygame.K_SPACE:
                        if can_do:
                            can_do = False
                        else:
                            can_do = True
                    if event.key == pygame.K_r and not can_do:
                        t = False
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    if event.key == pygame.K_LEFT:
                        if index > 0:
                            can_do = False
                            index -= 1
                            map_state, drones_state = turn[index]
                            turn_counter -= 1
                    if event.key == pygame.K_RIGHT:
                        if index < limit - 1:
                            can_do = False
                            index += 1
                            map_state, drones_state = turn[index]
                            turn_counter += 1
            if do_next_turn and can_do:
                try:
                    index += 1
                    if index == limit:
                        raise StopIteration
                    map_state, drones_state = turn[index]
                    turn_counter += 1
                except StopIteration:
                    can_do = False
                    index -= 1
            text = font.render(str(turn_counter), True, Color('black'))
            self.screen.blit(text, (50, 50))
            do_next_turn = self._render_map(map_state, drones_state)

        pygame.quit()
        return return_value
