from game import Game
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--size', type=int, default=20, help="the size of the grid, default: 20, min: 10, max: 50")
parser.add_argument('-b', '--bombs', type=float, default=0.15, help="the proportion of bombs in the grid, default: 0.15, min: 0.05, max: 0.35")
args = parser.parse_args()

if __name__ == "__main__":
    game = Game(args.size, args.bombs)
    game.go()
