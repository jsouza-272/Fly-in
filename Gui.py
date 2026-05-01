import pygame
from pygame.color import THECOLORS
from map import Map, Hub


class Gui():
    def __init__(self, map: Map, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        self.map = map
        self.screen = self._start()
        self.font = pygame.font.SysFont(None, 32)
        self.clock = pygame.time.Clock()

    def _start(self) -> pygame.Surface:
        pygame.init()
        return pygame.display.set_mode((self.width, self.height))

    def _render_map(self, map: list[Hub]):
        for hub in map:
            xy = (hub.xy[0] * 70 + 100, hub.xy[1] * 70 + 300)
            pygame.draw.rect(self.screen, pygame.Color('black'),
                             pygame.Rect(xy[0] - 20, xy[1] - 20, 40, 40),
                             border_radius=10)
            pygame.draw.circle(self.screen,
                               pygame.Color(hub.color.value),
                               xy, 21)
        pygame.display.flip()

    def loop(self):
        t = True
        retc = False
        while t:
            self.screen.fill(THECOLORS['grey40'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    t = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if not retc:
                            retc = True
                        else:
                            retc = False
                    if event.key == pygame.K_ESCAPE:
                        t = False
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
