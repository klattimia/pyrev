"""Reversi basic func."""


class rev_func:
    """
    Class _rev_func.

    useful funcion for class rev_core
    """

    def swap(self, turn, black, white):
        """Swap (black, white) to (player, opponent)."""
        if not turn:
            return black, white
        else:
            return white, black

    def swap_turn(self, turn):
        """Swap turn."""
        return 1 ^ turn

    def _legal_l(self, player, masked, blank, dir):
        """Direction << dir exploring."""
        tmp = masked & (player << dir)
        tmp |= masked & (tmp << dir)
        tmp |= masked & (tmp << dir)
        tmp |= masked & (tmp << dir)
        tmp |= masked & (tmp << dir)
        tmp |= masked & (tmp << dir)
        legal = blank & (tmp << dir)
        return legal

    def _legal_r(self, player, masked, blank, dir):
        """Direction >> dir exploring."""
        tmp = masked & (player >> dir)
        tmp |= masked & (tmp >> dir)
        tmp |= masked & (tmp >> dir)
        tmp |= masked & (tmp >> dir)
        tmp |= masked & (tmp >> dir)
        tmp |= masked & (tmp >> dir)
        legal = blank & (tmp >> dir)
        return legal

    def _reversed_l(self, player, masked, site, dir):
        """Direction << for self.reversed()."""
        rev = 0
        tmp = masked & (site << dir)
        blank = ~(player | masked)
        if tmp:
            for i in range(6):
                tmp <<= dir
                if tmp & blank:
                    break
                elif tmp & player:
                    rev |= tmp >> dir
                    break
                else:
                    tmp |= tmp >> dir
        return rev

    def _reversed_r(self, player, masked, site, dir):
        """Direction >> for self.reversed()."""
        rev = 0
        tmp = masked & (site >> dir)
        blank = ~(player | masked)
        if tmp:
            for i in range(6):
                tmp >>= dir
                if tmp & blank:
                    break
                elif tmp & player:
                    rev |= tmp << dir
                    break
                else:
                    tmp |= tmp << dir
        return rev

    def legal(self, turn, black, white):
        """Generate legal board."""
        player, opponent = self.swap(turn, black, white)
        blank = ~(black | white)
        h = opponent & 0x7e7e7e7e7e7e7e7e
        v = opponent & 0x00ffffffffffff00
        a = opponent & 0x007e7e7e7e7e7e00
        legal = self._legal_l(player, h, blank, 1)
        legal |= self._legal_l(player, v, blank, 8)
        legal |= self._legal_l(player, a, blank, 7)
        legal |= self._legal_l(player, a, blank, 9)
        legal |= self._legal_r(player, h, blank, 1)
        legal |= self._legal_r(player, v, blank, 8)
        legal |= self._legal_r(player, a, blank, 7)
        legal |= self._legal_r(player, a, blank, 9)
        return legal

    def reversed(self, turn, black, white, site):
        """Return reversed site board."""
        player, opponent = self.swap(turn, black, white)
        h = opponent & 0x7e7e7e7e7e7e7e7e
        v = opponent & 0x00ffffffffffff00
        a = opponent & 0x007e7e7e7e7e7e00
        rev = self._reversed_l(player, h, site, 1)
        rev |= self._reversed_l(player, v, site, 8)
        rev |= self._reversed_l(player, a, site, 7)
        rev |= self._reversed_l(player, a, site, 9)
        rev |= self._reversed_r(player, h, site, 1)
        rev |= self._reversed_r(player, v, site, 8)
        rev |= self._reversed_r(player, a, site, 7)
        rev |= self._reversed_r(player, a, site, 9)
        return rev

    def reverse(self, turn, black, white, site, rev):
        """Reverse board."""
        if not turn:
            return black ^ (rev ^ site), white ^ rev
        else:
            return black ^ rev, white ^ (rev ^ site)

    def count_stone(self, black, white):
        """Count stone."""
        nb = 0
        nw = 0
        while black:
            black &= black - 1
            nb += 1
        while white:
            white &= white - 1
            nw += 1
        return nb, nw
