import math

from constants import G, FRICTION


def move_ball(ball, dt):
    ball.pos_x += ball.v_x * dt
    ball.pos_y += ball.v_y * dt


def move_player(player, dt):
    move_ball(player, dt)
    player.v_x += player.a_x * dt


def apply_gravity(ball, dt):
    ball.v_y -= G * dt


def apply_horizontal_friction(ball):
    ball.v_x *= (1.0 - FRICTION)


def dot_product(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2


def handle_balls_collision(first_ball, second_ball, dt):
    v1x, v1y = first_ball.v_x, first_ball.v_y
    v2x, v2y = second_ball.v_x, second_ball.v_y
    x1, y1 = first_ball.pos_x, first_ball.pos_y
    x2, y2 = second_ball.pos_x, second_ball.pos_y
    m1, m2 = first_ball.mass, second_ball.mass

    coord_1 = 2.0 * m2 / (m1 + m2) * dot_product(v1x - v2x, v1y - v2y, x1 - x2, y1 - y2) / distance_square(x1 - x2,
                                                                                                           y1 - y2, 0.0,
                                                                                                           0.0)
    coord_2 = 2.0 * m1 / (m1 + m2) * dot_product(v2x - v1x, v2y - v1y, x2 - x1, y2 - y1) / distance_square(x2 - x1,
                                                                                                           y2 - y1, 0.0,
                                                                                                           0.0)

    first_ball.v_x -= coord_1 * (x1 - x2)
    first_ball.v_y -= coord_1 * (y1 - y2)

    second_ball.v_x -= coord_2 * (x2 - x1)
    second_ball.v_y -= coord_2 * (y2 - y1)

    if not first_ball.radius <= first_ball.pos_x + dt * first_ball.pos_x * first_ball.v_x <= 1.0 - first_ball.radius:
        first_ball.v_x = v1x
        second_ball.v_x = - v2x
    if not first_ball.radius <= first_ball.pos_y + dt * first_ball.pos_y * first_ball.v_y <= 1.0 - first_ball.radius:
        first_ball.v_y = v1y
        second_ball.v_y = - v2y
    if not second_ball.radius <= second_ball.pos_x + dt * second_ball.pos_x * second_ball.v_x <= 1.0 - second_ball.radius:
        second_ball.v_x = v2x
        first_ball.v_x = - v1x
    if not second_ball.radius <= second_ball.pos_y + dt * second_ball.pos_y * second_ball.v_y <= 1.0 - second_ball.radius:
        second_ball.v_y = v2y
        first_ball.v_y = - v1y


def handle_wall_collisions(ball):
    if ball.pos_x - ball.radius <= 0.0:
        ball.v_x = abs(ball.v_x)
        ball.pos_x = ball.radius
    elif ball.pos_x + ball.radius >= 1.0:
        ball.v_x = - abs(ball.v_x)
        ball.pos_x = 1.0 - ball.radius

    if ball.pos_y - ball.radius <= 0.0:
        ball.v_y = abs(ball.v_y)
        ball.pos_y = ball.radius
    elif ball.pos_y + ball.radius >= 1.0:
        ball.v_y = - abs(ball.v_y)
        ball.pos_y = 1.0 - ball.radius


def distance_square(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def are_balls_colliding(first_ball, second_ball):
    return distance_square(first_ball.pos_x, first_ball.pos_y, second_ball.pos_x,
                           second_ball.pos_y) - (first_ball.radius + second_ball.radius) ** 2 < - 0.001
