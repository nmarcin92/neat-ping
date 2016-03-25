import random

import time

from constants import SLEEP_TIME
from game_mechanic.objects import GameBall, PlayerBall, MoveType
from physics.dynamic import apply_gravity, move_ball, handle_wall_collisions, \
    apply_horizontal_friction, distance_square, are_balls_colliding, handle_balls_collision, move_player


class Simulation(object):
    def __init__(self, balls_nr):
        self.on_update = None

        self.player = PlayerBall()
        self.player.radius = 0.1
        self.player.pos_x = 0.23
        self.player.pos_y = 0.1
        self.player.mass = 10.0

        self.paused = False

        self.balls = []
        for i in range(balls_nr):
            ball = GameBall()
            ball.radius = 0.05
            ball.pos_x = random.random()
            ball.pos_y = random.random()
            ball.v_x = random.random() * 0.5
            ball.mass = 5.0
            self.balls.append(ball)

        self.player.v_x = 0.1

        self.balls.append(self.player)

    def on_player_move(self, move_type):
        if move_type == MoveType.LEFT:
            self.player.a_x = -0.01
        elif move_type == MoveType.RIGHT:
            self.player.a_x = 0.01
        elif move_type == MoveType.JUMP:
            self.player.is_jumping = True
            self.player.v_y = 0.3
        else:
            self.player.a_x = 0.0

    def iterate(self, dt):

        for b1 in self.balls:
            for b2 in self.balls:
                if b1 != b2 and not b1.is_handled_collision(b2) and are_balls_colliding(b1, b2):
                    handle_balls_collision(b1, b2, dt)
                    b1.mark_handled_collision(b2)

        for b1 in self.balls:
            for b2 in b1.handled_collisions:
                if not are_balls_colliding(b1, b2):
                    b1.unmark_handled_collision(b2)

        if self.player.v_y <= 0.0 and self.player.pos_y - self.player.radius < 0.0:
            self.player.is_jumping = False
            self.player.v_y = 0.0
            self.player.pos_y = self.player.radius

        for ball in self.balls:
            handle_wall_collisions(ball)
            apply_gravity(ball, dt)

        apply_horizontal_friction(self.player)

        for ball in self.balls[:-1]:
            move_ball(ball, dt)
        move_player(self.player, dt)

        self.on_update(self.player, self.balls[:-1])

    def start_loop(self, dt):
        while not self.paused:
            self.iterate(dt)
            time.sleep(SLEEP_TIME)
