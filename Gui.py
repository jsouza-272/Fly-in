import pygame
from pygame import Color
from map import Map, Hub, Link
from drones import Drone
from emulation import SimulationEngine


class Gui():
    def __init__(self, map: Map, title: str,
                 emulator: SimulationEngine,
                 width: int = 1280, height: int = 720,):
        self.width = width
        self.height = height
        self.map = map
        self.emulator = emulator
        self.screen = self._start(title)
        self.font = pygame.font.SysFont(None, 13)
        self.clock = pygame.time.Clock()

    def _start(self, title: str) -> pygame.Surface:
        pygame.init()
        pygame.display.set_caption(title)
        return pygame.display.set_mode((self.width, self.height))

    def _calc_scale(self, offset: int) -> int | float:
        map_x, map_y = self.map.map_size
        map_x = 1 if map_x == 0 else map_x
        map_y = 1 if map_y == 0 else map_y
        screen_x = self.screen.get_width() - 2*offset
        screen_y = self.screen.get_height() - 2*offset
        possible_scale = min(screen_x / map_x, screen_y / map_y)
        if possible_scale >= 70:
            scale = 70
        else:
            scale = possible_scale
        return scale

    def _render_links(self, links: list[Link], scale: int | float,
                      offset: int) -> None:
        for link in links:
            x1, y1 = link.zone1.xy
            x2, y2 = link.zone2.xy
            mx1 = (x1 * scale) + offset
            my1 = (self.screen.get_height() / 2) - (y1 * scale)
            mx2 = (x2 * scale) + offset
            my2 = (self.screen.get_height() / 2) - (y2 * scale)
            pygame.draw.line(self.screen, Color('black'),
                             (mx1, my1), (mx2, my2), 3)

    def _render_hubs(self, hubs: list[Hub], scale: int | float,
                     offset: int) -> None:
        for hub in hubs:
            x, y = hub.xy
            mx = (x * scale) + offset
            my = (self.screen.get_height() / 2) - (y * scale)
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
                       offset: int) -> None:
        for drone in drones:
            x, y = drone.coordinates
            mx = (x * scale) + offset
            my = (self.screen.get_height() / 2) - (y * scale)
            points = [(mx, my + 10), (mx + 10, my),
                      (mx, my - 10), (mx - 10, my)]
            pygame.draw.polygon(self.screen, Color((0, 255, 255)),
                                points)
            txt = self.font.render(drone.name, True,
                                   Color("black"))
            self.screen.blit(txt, (mx-5, my-2))

    def _render_map(self, map_state: Map, drones_state: list[Drone]):
        offset = 50
        scale = self._calc_scale(offset)
        set_link = set([link for hub in map_state.map
                        for link in hub.links.values()])
        self._render_links(set_link, scale, offset)
        self._render_hubs(map_state.map, scale, offset)
        self._render_drones(drones_state[::-1], scale, offset)
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
            self.screen.fill(Color('grey40'))
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
