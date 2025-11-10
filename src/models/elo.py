import math
from collections import defaultdict

class EloModel:
    def __init__(self, base=1500, k=20, home_adv=55):
        self.ratings = defaultdict(lambda: base)
        self.k = k
        self.home_adv = home_adv

    @staticmethod
    def _win_prob(r_a, r_b):
        return 1.0 / (1.0 + 10 ** ((r_b - r_a) / 400))

    def game(self, home, away, home_pts, away_pts):
        r_home = self.ratings[home] + self.home_adv
        r_away = self.ratings[away]
        p_home = self._win_prob(r_home, r_away)
        home_win = 1.0 if home_pts > away_pts else 0.0

        mov = abs(home_pts - away_pts)
        mult = math.log(max(mov,1)+1) * (2.2 / ((r_home - r_away) * 0.001 + 2.2))

        delta = self.k * mult * (home_win - p_home)
        self.ratings[home] += delta
        self.ratings[away] -= delta
