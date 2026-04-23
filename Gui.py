import pygame
from map import Map, Hub, Link


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
            pygame.draw.circle(self.screen,
                               pygame.color.THECOLORS[hub.color.value],
                               xy, 20)
        pygame.display.flip()

    def loop(self):
        t = True
        while t:
            self.clock.tick()
            fps = self.clock.get_fps()
            text = self.font.render(str(round(fps, 1)), True, pygame.color.THECOLORS['black'])
            self.screen.fill(pygame.color.THECOLORS['grey40'])
            self.screen.blit(text, (20, 20))
            self._render_map(self.map.map)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    t = False
        pygame.quit()
