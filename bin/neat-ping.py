from constants import BALLS_NR
from game_graphics.window import GameWindow
from game_mechanic.mechanic import Simulation


def main():
    simulation = Simulation(BALLS_NR)
    game_win = GameWindow(simulation)
    game_win.run_simulation()


if __name__ == '__main__':
    main()
