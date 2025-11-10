import random
from pathlib import Path

import pandas as pd
import typer

from models.elo import EloModel

app = typer.Typer(add_completion=False)


def load_ratings(path: str = "outputs/elo_ratings.csv") -> dict:
    """Load team Elo ratings from CSV into a dict."""
    s = pd.read_csv(path, index_col=0).iloc[:, 0]
    return {k: float(v) for k, v in s.items()}


def sim_once(teams: list[str], elo: EloModel) -> str:
    """
    Simulate one single-elimination bracket.
    Handles odd team counts by giving the last team a bye.
    Returns the champion team name.
    """
    rnd = teams[:]  # working copy
    random.shuffle(rnd)

    while len(rnd) > 1:
        nxt: list[str] = []

        # If odd number of teams, last team gets a bye (auto-advance)
        if len(rnd) % 2 == 1:
            nxt.append(rnd.pop())

        # Pair safely: stop at len(rnd) - 1 so i+1 is valid
        for i in range(0, len(rnd) - 1, 2):
            a, b = rnd[i], rnd[i + 1]
            # Use EloModel's win-prob method with CURRENT ratings
            p = EloModel._win_prob(elo.ratings[a], elo.ratings[b])
            nxt.append(a if random.random() < p else b)

        rnd = nxt

    return rnd[0]


@app.command()
def main(season: int = 2026, runs: int = 5000) -> None:
    # 1) Load ratings and seed Elo model
    ratings = load_ratings()
    elo = EloModel()
    elo.ratings.update(ratings)

    # 2) Pick playoff field (top 8 by Elo to keep bracket even/clean)
    teams = [t for t, _ in sorted(ratings.items(), key=lambda x: x[1], reverse=True)[:8]]
    if len(teams) < 2:
        raise ValueError(f"Need at least 2 teams, found {len(teams)} from ratings.")

    # 3) Run simulations
    wins = {t: 0 for t in teams}
    for _ in range(runs):
        winner = sim_once(teams, elo)
        wins[winner] += 1

    # 4) Export results
    out = (
        pd.DataFrame({"team": list(wins.keys()),
                      "win_prob": [w / runs for w in wins.values()]})
        .sort_values("win_prob", ascending=False)
        .reset_index(drop=True)
    )

    out_path = Path("outputs") / f"sb_probs_{season}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)

    print(out.head(10))
    print(f"[sim] Saved results → {out_path}")


if __name__ == "__main__":
    # Allow running without specifying a subcommand:
    #   python src/simulate_playoffs.py --season 2023 --runs 5000
    typer.run(main)
