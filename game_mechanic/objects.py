from physics.objects import Ball


class GameBall(Ball):
    def __init__(self):
        super(GameBall, self).__init__()
        self.handled_collisions = []

    def is_handled_collision(self, other):
        return self in other.handled_collisions or other in self.handled_collisions

    def mark_handled_collision(self, other):
        self.handled_collisions.append(other)
        other.handled_collisions.append(self)

    def unmark_handled_collision(self, other):
        self.handled_collisions.remove(other)
        other.handled_collisions.remove(self)


class PlayerBall(GameBall):
    def __init__(self):
        super(PlayerBall, self).__init__()
        self.is_jumping = False
        self.a_x = 0.0


class MoveType(object):
    RIGHT, LEFT, JUMP, RESET = range(4)