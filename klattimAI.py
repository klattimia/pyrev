"""CNN for Reversi."""
# from keras.models import Sequential, Model
# from keras.layers import Dense, Dropout, Activation, Flatten
# from keras.layers import Conv2D, MaxPooling2D
# import numpy as np
from pyrev.func import rev_func


class rev_branch(rev_func):
    """Create possible branch."""

    def next_branch(self, turn, board_list):
        """
        Create next board_list.

        board_list = [(bl1, wh1),
                      (bl2, wh2),
                      ...,
                      (bln, whn)]
        """
        next_board = set()
        for bl, wh in board_list:
            x = self.legal(turn, bl, wh)
            if not x:
                next_board.add((bl, wh))
            while x:
                y = x & (x - 1)
                x, z = y, x ^ y
                rev = self.reversed(turn, bl, wh, z)
                bl, wh = self.reverse(turn, bl, wh, z, rev)
                next_board.add((bl, wh))
        return self.swap_turn(turn), list(next_board)

    def gen_depth_k(self, k, turn, board_list):
        """Create depth k branch."""
        for i in range(k):
            turn, board_list = self.next_branch(turn, board_list)
        return turn, board_list

    def decided_or(self, flags):
        """Black win."""
        if True in flags:
            return True
        return False

    def decided_and(self, flags):
        """Black win."""
        if False in flags:
            return False
        return True

    def gen_flags(self, which_win, board):
        """
        Generate flags against ended board.

        which = 0(black) or 1(white)
        """
        bl, wh = board
        nb, nw = self.count_stone(bl, wh)
        if nb > nw:
            if not which_win:
                return True
            else:
                return False
        elif nb < nw:
            if not which_win:
                return False
            else:
                return True
        else:
            return False

    def decided_k(self, k, which_win, turn, board):
        """Black win."""
        if k < 1:
            return self.gen_flags(which_win, board)
        turn, boards = self.next_branch(turn, [board])
        flags = [self.decided_k(k-1, which_win, turn, x) for x in boards]
        if not turn & which_win:
            return self.decided_or(flags)
        else:
            return self.decided_and(flags)


if __name__ == '__main__':
    branch = rev_branch()
    a = branch.decided_k(
        30, 0, 0, (0x18b07c70181a0203, 0x4706020f06247d3c))
    print(a)

# class trans_bit_array:
#     """Translation from bitboard to array."""
#
#     def make_array(bitboard):
#         """Make an array."""
#         array = [bitboard & (1 << i) for i in range(64)]
#         return np.reshape(array, (8, 8))
#
#
# class train:
#     """train the conv_model"""
#
#     def conv_model(self, data_shape=(5000, 8, 8)):
#         model = Sequential()
#         model.add(Conv2D(16, (3, 3), activation='relu'))
#         model.add(Conv2D(16, (3, 3), activation='relu'))
#         model.add(MaxPooling2D(pool_size=(2, 2)))
#         model.add(Dropout(0.25))
#         model.add(Conv2D(64, (3, 3), activation='relu'))
#         model.add(Conv2D(64, (3, 3), activation='relu'))
#         model.add(MaxPooling2D(pool_size=(2, 2)))
#         model.add(Flatten())
#         model.add(Dense(512, activation='relu'))
#         model.add(Dropout(0.5))
#         model.add(Dense())
#         model.add(Activation('softmax'))
#         return model
#
#     def reshape_data(raw_data, ):
#         train_X = np.reshape(input_data, (-1, 64, 1))
#         train_Y = np.reshape(output_data, (-1, 16, 1))
