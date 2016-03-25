import threading

import pygame
import thread

from constants import DT


class GameWindow(object):
    def __init__(self, simulation):
        self.simulation = simulation
        self.simulation.on_update = self.on_update
        self.screen = pygame.display.set_mode((800, 800))

        self.ball_color = (255, 0, 0)
        self.player_color = (0, 255, 0)

    def run_simulation(self):
        threading.Thread(target=self.listen_for_keys).start()
        threading.Thread(target=self.simulation.start_loop, args=(DT,)).start()

    def listen_for_keys(self):
        while True:
            for event in pygame.event.get():
                print event

    def on_update(self, player, balls):
        self.screen.fill((255, 255, 255))
        for ball in balls:
            self.draw_ball(ball, self.ball_color)

        self.draw_ball(player, self.player_color)

        pygame.display.update()

    def draw_ball(self, ball, color):
        pygame.draw.circle(self.screen, color, (int(round(ball.pos_x * 800)), int(round((1.0 - ball.pos_y) * 800))),
                           int(round(ball.radius * 800)), 0)
