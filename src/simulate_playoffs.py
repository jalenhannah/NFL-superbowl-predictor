import random
from pathlib import Path
import pandas as pd
import typer
from models.elo import EloModel

app = typer.Typer(add_completion=False)

def load_ratings(path="outputs/elo_ratings.csv"):
    s = pd.read_csv(path, index_col=0).iloc[:,0]
    return {k:v for k,v in s.items()}

@app.command()
def main(season: int = 2026, runs: int = 5000):
    ratings = load_ratings()
    elo = EloModel()
    elo.ratings.update(ratings)

    teams = [t for t,_ in sorted(ratings.items(), key=lambda x: x[1], reverse=True)[:14]]

    def sim_once():
        bracket = teams[:]
        random.shuffle(bracket)
        while len(bracket) > 1:
            nxt = []
            for i in range(0, len(bracket), 2):
                a, b = bracket[i], bracket[i+1]
                p = elo._win_prob(elo.ratings[a], elo.ratings[b])
                nxt.append(a if random.random() < p else b)
            bracket = nxt
        return bracket[0]

    wins = {t:0 for t in teams}
    for _ in range(runs):
        wins[sim_once()] += 1

    out = pd.DataFrame({"team": list(wins.keys()),
                        "sb_prob": [wins[t]/runs for t in wins]}) \
            .sort_values("sb_prob", ascending=False)

    Path("outputs").mkdir(parents=True, exist_ok=True)
    out_path = f"outputs/sb_probs_{season}.csv"
    out.to_csv(out_path, index=False)
    print(out.head(10))
    print(f"Saved → {out_path}")

if __name__ == "__main__":
    app()
