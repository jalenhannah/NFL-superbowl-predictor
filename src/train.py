import pandas as pd
from pathlib import Path
from models.elo import EloModel

def train_from_csv(in_path="data/games.csv", out_path="outputs/elo_ratings.csv"):
    df = pd.read_csv(in_path).sort_values(["season","week"])
    elo = EloModel()
    for _, r in df.iterrows():
        elo.game(r["home"], r["away"], r["home_pts"], r["away_pts"])
    Path("outputs").mkdir(parents=True, exist_ok=True)
    pd.Series(elo.ratings).sort_values(ascending=False).to_csv(out_path, header=["elo"])
    print(f"Saved ratings → {out_path}")

if __name__ == "__main__":
    train_from_csv()
def main():
    print("✅ train.py started")

if __name__ == "__main__":
    main()
