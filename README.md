# CLI minesweeper

This project is about developing a minesweeper played with a command line interface.

To launch the script type the following command:
> python3 minesweeper.py [grid size] [bombs proportion]

The game is played with VIM controls:
* h: deplace cursor left
* j: deplace cursor down
* k: deplace cursor up
* l: deplace cursor right
* space: reveal a cell, except if there is a flag on
* f: place a flag
* a: reveal all the cells around the selected cell, except where there are flags on
