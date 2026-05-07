import pygame
from pygame.color import THECOLORS
from map import Map, Hub, Link


class Gui():
    def __init__(self, map: Map, title: str,
                 width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        self.map = map
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

    def _render_link(self, links: list[Link], scale: int | float,
                     offset: int) -> None:
        for link in links:
            x1, y1 = link.zone1.xy
            x2, y2 = link.zone2.xy
            nx1 = (x1 * scale) + offset
            ny1 = (self.screen.get_height() / 2) - (y1 * scale)
            nx2 = (x2 * scale) + offset
            ny2 = (self.screen.get_height() / 2) - (y2 * scale)
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (nx1, ny1), (nx2, ny2), 3)

    def _render_map(self, map: list[Hub]):
        offset = 50
        scale = self._calc_scale(offset)
        set_link = set([link for hub in map for link in hub.links.values()])
        self._render_link(set_link, scale, offset)
        for hub in map:
            x, y = hub.xy
            nx = (x * scale) + offset
            ny = (self.screen.get_height() / 2) - (y * scale)
            pygame.draw.rect(self.screen, pygame.Color('black'),
                             pygame.Rect(nx - 20, ny - 20, 40, 40),
                             border_radius=10)
            pygame.draw.circle(self.screen,
                               pygame.Color(hub.color.value),
                               (nx, ny), 21)
            self.screen.blit(self.font.render(hub.name, True,
                                              pygame.Color('white')),
                             (nx - 30, ny + 25))
        pygame.display.flip()

    def loop(self):
        t = True
        retc = False
        return_value = ''
        while t:
            self.screen.fill(pygame.Color('grey40'))
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

            if retc:
                pygame.draw.line(self.screen, THECOLORS['black'],
                                 (70, 70), (150, 150), 10)
            self.clock.tick()
            fps = self.clock.get_fps()
            text = self.font.render(str(round(fps, 1)), True,
                                    THECOLORS['black'])
            self.screen.blit(text, (20, 20))
            self._render_map(self.map.map)

        pygame.quit()
        return return_value
