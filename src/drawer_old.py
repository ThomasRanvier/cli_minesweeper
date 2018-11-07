from termcolor import colored
import time
import sys
import os

class Drawer():
    def __init__(self, size):
        self.__size = size
        self.__clear = True
    
    def __del__(self):
        if self.__clear:
            os.system('clear')
    
    def draw(self, grid, grid_mask, cursor, shockwave=None, clean=True):
        for y in range(self.__size):
            line = ''
            for x in range(self.__size):
                char, color, bold, background = self.__get_cell(x, y, cursor, grid, grid_mask, shockwave)
                if bold and background != None:
                    char = colored(char, color, background, attrs=['bold'])
                elif bold and background == None:
                    char = colored(char, color, attrs=['bold'])
                elif not bold and background != None:
                    char = colored(char, color, background)
                else:
                    char = colored(char, color)
                line += char
                if x < self.__size - 1:
                    line += ' '
            print(line + '\033[K')
        if self.__clear:
            sys.stdout.write(self.__size * '\033[F')

    def __get_cell(self, x, y, cursor, grid, grid_mask, shockwave=None):
        char = '#'
        color = 'grey'
        bold = False
        background = None
        added = False
        if shockwave != None:
            if shockwave[x][y] == 2:
                background = 'on_red'
                bold = True
                added = True
            elif shockwave[x][y] == 3:
                color = 'red'
                added = True
        if not added:
            if grid_mask[x][y] == 1:
                if grid[x][y] > 0:
                    char = grid[x][y]
                    if grid[x][y] == 1:
                        color = 'blue'
                    elif grid[x][y] == 2:
                        color = 'green'
                    elif grid[x][y] == 3:
                        color = 'magenta'
                    elif grid[x][y] == 4:
                        color = 'cyan'
                    elif grid[x][y] == 5:
                        color = 'yellow'
                    elif grid[x][y] == 6:
                        color = 'blue'
                    elif grid[x][y] == 7:
                        color = 'green'
                    elif grid[x][y] == 8:
                        color = 'magenta'
                elif grid[x][y] == 0:
                    char = ' '
                elif grid[x][y] == -1:
                    char = 'o'
                    color = 'red'
            elif grid_mask[x][y] == 2:
                char = 'F'
                color = 'cyan'
                bold = True
        if x == cursor['x'] and y == cursor['y']:
            background = 'on_white'
            bold = True
        return (char, color, bold, background)

    def display_end_screen(self, statut, grid, grid_mask, cursor):
        if statut == 'lost':
            self.__display_shockwave(grid, grid_mask, cursor)
        self.__quit(grid, grid_mask, statut)

    def __quit(self, grid, grid_mask, statut):
        self.__clear = False
        self.draw(grid, grid_mask, {'x': -1, 'y':-1})
        print('')
        sys.stdout.write('\033[F\033[K')
        print('\n')
        print('You lost, :/' if statut == 'lost' else 'GG, you won ! :)')
        print('\n')
        
    def __display_shockwave(self, grid, grid_mask, cursor):
        shockwave_out = False
        shockwave = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
        iterations = 0
        while not shockwave_out:
            if iterations == 0 or iterations == 2 or iterations == 4 or iterations == 6 or iterations == 8:
                shockwave[cursor['x']][cursor['y']] = 2
            self.draw(grid, grid_mask, {'x': -1, 'y':-1}, shockwave)
            to_update_to_2 = []
            shockwave_out = True
            for x in range(self.__size):
                for y in range(self.__size):
                    if shockwave[x][y] == 2:
                        shockwave_out = False
                        if x > 0:
                            if shockwave[x - 1][y] == 0:
                                shockwave[x - 1][y] = 1
                                to_update_to_2.append((x - 1, y))
                        if y > 0:
                            if shockwave[x][y - 1] == 0:
                                shockwave[x][y - 1] = 1
                                to_update_to_2.append((x, y - 1))
                        if x < self.__size - 1:
                            if shockwave[x + 1][y] == 0:
                                shockwave[x + 1][y] = 1
                                to_update_to_2.append((x + 1, y))
                        if y < self.__size - 1:
                            if shockwave[x][y + 1] == 0:
                                shockwave[x][y + 1] = 1
                                to_update_to_2.append((x, y + 1))
                        shockwave[x][y] = 3
            for x, y in to_update_to_2:
                grid_mask[x][y] = 1
                shockwave[x][y] = 2
            for x in range(self.__size):
                for y in range(self.__size):
                    if shockwave[x][y] == 3:
                        exploding_in_neighbourhood = False
                        if x > 0:
                            if shockwave[x - 1][y] == 2:
                                exploding_in_neighbourhood = True
                        if y > 0:
                            if shockwave[x][y - 1] == 2:
                                exploding_in_neighbourhood = True
                        if x < self.__size - 1:
                            if shockwave[x + 1][y] == 2:
                                exploding_in_neighbourhood = True
                        if y < self.__size - 1:
                            if shockwave[x][y + 1] == 2:
                                exploding_in_neighbourhood = True
                        if not exploding_in_neighbourhood:
                            shockwave[x][y] = 0
            time.sleep(0.05)
            iterations += 1
