#!/usr/bin/python
"""UI for Reversi."""


import random
from pyrev.pycolor import pycolor
from pyrev.core import rev_core


class rev_ui(rev_core):
    """Class rev_ui.

    Provide User Interface to play game
    """

    def __init__(self):
        """Define the first state."""
        super().__init__(0, 0x0000001008000000, 0x0000000810000000)

    def show_board(self):
        """Show the board for command line."""
        print("—" * 38)
        for i in range(10):
            for j in range(10):
                mask = 2**(63-(j-1)-8*(i-1))
                if i == 0 or i == 9:
                    if j == 0 or j == 9:
                        print(" ", end=" | ")
                    else:
                        print(pycolor.RED + str(j) + pycolor.END, end=" | ")
                elif j == 0 or j == 9:
                    print(pycolor.RED + str(i) + pycolor.END, end=" | ")
                elif mask & self.black:
                    print("🔵", end=" | ")
                elif mask & self.white:
                    print("⚪️", end=" | ")
                elif mask & self.judge:
                    print("x", end=" | ")
                else:
                    print(" ", end=" | ")
            print("\n" + "-" * 38)
        print(hex(self.black), hex(self.white))

    def show_stone(self):
        """Show the number of stones."""
        nb, nw = self.count_board()
        print("Black:{} vs White:{}".format(nb, nw))

    def show_result(self):
        """Show the result."""
        nb, nw = self.count_board()
        if nb == nw:
            print("Game over\tDraw")
        else:
            winner = "Black" if nb > nw else "White"
            print("Game Over\t{} Won".format(winner))

    def input_player(self):
        """Player input site."""
        while True:
            raw_site = input('ij:(row, col) = (i, j), 0:undo  >>> ')
            try:
                _site = int(raw_site)
            except Exception as e:
                print(e)
                continue
            row, col = (_site // 10), (_site % 10)
            if 0 < row < 9 and 0 < col < 9:
                site = 2**(63-(col-1)-8*(row-1))
                if self.judge & site:
                    self.add_site(site)
                    break
            elif not _site:
                if self.put:
                    self.undo()
                    self.show_board()
                else:
                    print("It has already been initialized")
            else:
                print("You cannot put there")

    def input_random(self):
        """Random input site."""
        while True:
            site = 1 << random.randrange(0, 64)
            if self.judge & site:
                self.add_site(site)
                break

    def input(self, black, white):
        """Define input way of each side."""
        if not self.turn:
            black()
        else:
            white()

    def jud_end(self):
        """Judge whether end."""
        self.insert_judge()
        if not self.judge:
            self.next_turn()
            self.insert_judge()
            if not self.judge:
                return True
            else:
                self.caution_pass()
                return False
        else:
            return False

    def caution_pass(self):
        """Caution to pass."""
        print("turn passed")

    def game_flow(self):
        """Game flow of reversi."""
        while True:
            if self.jud_end():
                # turn has already been changed by self.jud_end()
                # legal board has already been generated
                self.show_board()
                self.show_stone()
                self.show_result()
                break
            self.show_board()
            self.show_stone()
            self.input(self.input_player, self.input_random)
            self.next_board()
            self.next_turn()


if __name__ == '__main__':
    game = rev_ui()
    game.game_flow()
