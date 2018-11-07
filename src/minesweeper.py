from game import Game
from bot import Bot
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--size', type=int, default=20, help="the size of the grid, default: 20, min: 10, max: 50")
parser.add_argument('-b', '--bombs', type=float, default=0.15, help="the proportion of bombs in the grid, default: 0.15, min: 0.05, max: 0.35")
parser.add_argument('-a', '--ai', action='store_true', help="if added a bot will play the game")
args = parser.parse_args()

if __name__ == "__main__":
    game = Game(args.size, args.bombs)
    if args.ai:
        bot = Bot(game)
        bot.play()
    else:
        game.play_as_player()
