import pygame
from pygame import Color
from map import Map, Hub, Link
from drones import Drone
from emulation import SimulationEngine


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
        self.emulator = emulator
        self.screen = self._start(title)
        self.font = pygame.font.SysFont(None, 13)
        self.clock = pygame.time.Clock()

    def _start(self, title: str) -> pygame.Surface:
        fullscreen = 0
        if (self.height == pygame.display.Info().current_h
            and self.width == pygame.display.Info().current_w):
            fullscreen = pygame.FULLSCREEN
        pygame.display.set_caption(title)
        return pygame.display.set_mode((self.width, self.height), fullscreen)

    def calc_scale_and_offset(self, padding) -> tuple[float, tuple]:
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
        for link in links:
            x1, y1 = link.zone1.xy
            x2, y2 = link.zone2.xy
            mx1 = (x1 * scale) + off_x
            my1 = (y1 * scale) + off_y
            mx2 = (x2 * scale) + off_x
            my2 = (y2 * scale) + off_y
            pygame.draw.line(self.screen, Color('black'),
                             (mx1, my1), (mx2, my2), 3)

    def _render_hubs(self, hubs: list[Hub], scale: int | float,
                     offset: tuple) -> None:
        off_x, off_y = offset
        for hub in hubs:
            x, y = hub.xy
            mx = (x * scale) + off_x
            my = (y * scale) + off_y
            pygame.draw.rect(self.screen, Color('black'),
                             pygame.Rect(mx - 20, my - 20, 40, 40),
                             border_radius=10)
            pygame.draw.circle(self.screen,
                               Color(hub.color.value),
                               (mx, my), 21)
            self.screen.blit(self.font.render(hub.name, True,
                                              Color('white')),
                             (mx - 30, my + 25))

    def _render_drones(self, drones: list[Drone], scale: int | float,
                       offset: float) -> None:
        off_x, off_y = offset
        old_coords = set()
        for drone in drones:
            x, y = drone.coordinates
            if (x, y) in old_coords:
                continue
            mx = (x * scale) + off_x
            my = (y * scale) + off_y
            border = [(mx, my + 12), (mx + 12, my),
                      (mx, my - 12), (mx - 12, my)]
            points = [(mx, my + 10), (mx + 10, my),
                      (mx, my - 10), (mx - 10, my)]
            pygame.draw.polygon(self.screen, Color('gray30'),
                                border)
            pygame.draw.polygon(self.screen, Color('gray50'),
                                points)
            txt = self.font.render(drone.name, True,
                                   Color("black"))
            self.screen.blit(txt, (mx-5, my-2))
            old_coords.add((x, y))
            print(old_coords)

    def _render_map(self, map_state: Map, drones_state: list[Drone]):
        scale, offset = self.calc_scale_and_offset(300)
        set_link = set([link for hub in map_state.map
                        for link in hub.links.values()])
        self._render_links(set_link, scale, offset)
        self._render_hubs(map_state.map, scale, offset)
        self._render_drones(drones_state, scale, offset)
        pygame.display.flip()

    def loop(self):
        t = True
        retc = False
        can_do = False
        return_value = ''
        turn = self.emulator.turn()
        map_state, drones_state = self.map, self.map.start_hub.drones
        counter = 0
        time_limit = 12
        while t:
            self.clock.tick(12)
            self.screen.fill(Color('gray80'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    t = False
                    return_value = 'q'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if not retc:
                            retc = True
                        else:
                            retc = False
                    if event.key == pygame.K_ESCAPE:
                        t = False
                        return_value = 'q'
                    if event.key == pygame.K_n:
                        t = False
                        return_value = 'n'
                    if event.key == pygame.K_b:
                        t = False
                        return_value = 'b'
                    if event.key == pygame.K_SPACE:
                        if can_do:
                            can_do = False
                        else:
                            can_do = True
                    if event.key == pygame.K_s:
                        if time_limit == 12:
                            time_limit = 0
                        else:
                            time_limit == 12

            if retc:
                pygame.draw.line(self.screen, Color('black'),
                                 (70, 70), (150, 150), 10)
            if can_do:
                counter += 1
            if counter >= time_limit:
                counter = 0
                try:
                    map_state, drones_state = next(turn)
                except StopIteration:
                    can_do = False
            self.clock.tick()
            fps = self.clock.get_fps()
            text = self.font.render(str(round(fps, 1)), True,
                                    Color('black'))
            self.screen.blit(text, (20, 20))
            self._render_map(map_state, drones_state)

        pygame.quit()
        return return_value
