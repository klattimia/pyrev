"""Core of Reversi implementation."""
import numpy as np
import random
from pyrev.klattimAI import rev_branch


class rev_core(rev_branch):
    """
    Class rev_core.

    bitboard is used
    """

    def __init__(self, turn, black, white):
        """Generate initial board."""
        self.turn = turn
        self.black = black
        self.white = white
        self.blank = ~(self.black | self.white)
        self.put = []
        self.rev = []

    def next_board(self):
        """Reverse self.black and self.white."""
        self.black, self.white = self.reverse(
            self.turn, self.black, self.white, self.put[-1], self.rev[-1])

    def next_turn(self):
        """Swap self.turn."""
        self.turn ^= 1

    def add_site(self, site):
        """Append self.put and self.rev."""
        self.put.append(site)
        self.rev.append(
            self.reversed(self.turn, self.black, self.white, site))

    def add_0(self):
        """
        Fix behavior of undo which follows after pass.

        This is called When the turn is passed
        without this func, undo would behave incorrectly
        """
        self.put.append(0)
        self.rev.append(0)

    def insert_judge(self):
        """Inseert legal board to self.judge."""
        self.judge = self.legal(self.turn, self.black, self.white)

    def undo(self):
        """Undo self.black and self.white."""
        self.next_turn()
        self.next_board()
        self.insert_judge()
        self.put, self.rev = self.put[:-1], self.rev[:-1]

    def count_board(self):
        """Count stone on self.black and self.white."""
        return self.count_stone(self.black, self.white)

    def input_random(self, opt_args):
        """Random input site."""
        while True:
            site = 1 << random.randrange(0, 64)
            if self.judge & site:
                self.add_site(site)
                break

    def input_random_w(self, w):
        """Random generate under weight of w."""
        w = np.array(w) / sum(w)
        while True:
            site = 1 << int(np.random.choice(range(64), p=w))
            if self.judge & site:
                self.add_site(site)
                break

    def input_decided_k(self, last_k=10, which_win=1):
        """
        Use decided flag.

        args = (last_k, which_win)
        """
        def outer(func):
            def inner(*args, **kwargs):
                nb, nw = self.count_board()
                if last_k + nb + nw > 64:
                    turn, boards = \
                        self.next_branch(self.turn, [(self.black, self.white)])
                    for x in boards:
                        if self.decided_k(2*last_k, which_win, turn, x):
                            site = (x[0] ^ self.black) ^ (x[1] ^ self.white)
                            self.add_site(site)
                            break
                        elif x == boards[-1]:
                            func(*args, **kwargs)
                else:
                    func(*args, **kwargs)
            return inner
        return outer

    def input(self, black_func, white_func, black_args, white_args):
        """Decorate input function to sync with turn."""
        if not self.turn:
            black_func(black_args)
        else:
            white_func(white_args)

    def jud_end(self):
        """Judge whether end."""
        self.insert_judge()
        if not self.judge:
            self.next_turn()
            self.insert_judge()
            if not self.judge:
                return True
            else:
                self.add_0()
                return False
        else:
            return False

    def game_flow_noprint(self, black_f, white_f, black_args, white_args):
        """Game flow without print."""
        count = [0, 0]
        while True:
            if self.jud_end():
                nb, nw = self.count_board()
                id = 0 if nb > nw else 1
                count[id] += 1
                print(count)
                self.__init__()
                continue
            self.input(black_f, white_f, black_args, white_args)
            self.next_board()
            self.next_turn()
