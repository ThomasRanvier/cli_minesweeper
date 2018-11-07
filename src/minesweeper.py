from game import Game
import sys

if __name__ == "__main__":
    game = Game(int(sys.argv[1]), float(sys.argv[2]))
    game.go()
