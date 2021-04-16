import pygame
import sys


class SpaceInvaders:

    set_screen = None
    enemies=[]

    def __init__(self, window_height, window_width):
        pygame.init()
        self.window_height = window_height
        self.window_width = window_width
        close_button = False
        self.enemies=[]

        self.set_screen = pygame.display.set_mode(
            (window_height, window_width))


        self.clock = pygame.time.Clock()
        margin = 30 
        width = 50 
        for x in range(margin,self.window_width - margin, width):
            for y in range(margin, int(self.window_height / 2), width):
                self.enemies.append(Enemies(self.set_screen, 50, 50))

        while not close_button:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close_button = True

            self.clock.tick(60)
            pygame.display.flip()

            self.set_screen.fill((0, 0, 0))

            for enemy in self.enemies:

                enemy.draw_enemies()


class Enemies:

    def __init__(self, screen, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen

    def draw_enemies(self):

        pygame.draw.rect(self.screen, (0, 0, 255), (self.x_pos,self.y_pos, 50, 50))
        self.y_pos+=0.05
        print(self.x_pos,"   ",self.y_pos)


if __name__ == "__main__":
    # pygame.display.list_modes()
    # screen = SpaceInvaders(600, 400)
    screen = SpaceInvaders(1280, 768)
    # screen.enemies.draw_enemies()
