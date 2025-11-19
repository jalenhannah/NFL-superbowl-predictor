"""
train.py

Train Elo ratings from historical NFL game results and save them to a CSV file.

This script:
1. Loads game results from a CSV file (e.g., data/games.csv)
2. Uses an Elo model to update team ratings over time
3. Saves the final ratings to outputs/elo_ratings.csv (by default)

Run from the command line, for example:

    python train.py --games-path data/games.csv --output-path outputs/elo_ratings.csv
"""

import logging
from pathlib import Path

import pandas as pd
import typer

from models.elo import EloModel  # Uses your EloModel with .game() and .ratings

app = typer.Typer(add_completion=False)

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def load_games(path: Path) -> pd.DataFrame:
    """
    Load NFL game data from a CSV file.

    Args:
        path: Path to the games.csv file.

    Returns:
        A pandas DataFrame containing the game data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"Games file not found at: {path}")

    logging.info(f"Loading games from {path}...")
    df = pd.read_csv(path)

    # Match your actual CSV columns:
    # season, week, home, away, home_pts, away_pts
    required_cols = {
        "season",
        "week",
        "home",
        "away",
        "home_pts",
        "away_pts",
    }

    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing expected columns in games.csv: {missing}. "
            f"Available columns are: {list(df.columns)}"
        )

    # Sort games in chronological order (season, week)
    df = df.sort_values(["season", "week"]).reset_index(drop=True)

    logging.info(f"Loaded {len(df)} games.")
    return df


def train_elo_model(games: pd.DataFrame) -> dict:
    """
    Train an Elo model on the game data and return the final team ratings.

    Args:
        games: DataFrame of historical game results.

    Returns:
        A dictionary mapping team name -> Elo rating.
    """
    logging.info("Initializing Elo model...")

    # Create a new EloModel instance (from your elo.py)
    elo = EloModel()

    # Loop through each game and update the Elo ratings
    for _, row in games.iterrows():
        home_team = row["home"]
        away_team = row["away"]
        home_score = row["home_pts"]
        away_score = row["away_pts"]

        # Use your EloModel.game(...) method to process each game
        elo.game(
            home=home_team,
            away=away_team,
            home_pts=home_score,
            away_pts=away_score,
        )

    # Your EloModel stores ratings in self.ratings (a defaultdict)
    ratings = dict(elo.ratings)

    logging.info(f"Trained Elo model for {len(ratings)} teams.")
    return ratings


def save_ratings(ratings: dict, path: Path) -> None:
    """
    Save Elo ratings to a CSV file.

    Args:
        ratings: Dict mapping team -> Elo rating.
        path: Output path for elo_ratings.csv
    """
    if not ratings:
        logging.warning(
            "No ratings to save. The Elo model may not have been trained correctly."
        )

    # Convert the dict into a pandas Series for easy CSV export
    s = pd.Series(ratings, name="elo")
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists
    s.to_csv(path)
    logging.info(f"Saved Elo ratings to {path}")


@app.command()
def main(
    games_path: Path = typer.Option(
        Path("data/games.csv"),
        help="Path to the games.csv file with historical results.",
    ),
    output_path: Path = typer.Option(
        Path("outputs/elo_ratings.csv"),
        help="Path to save the Elo ratings CSV.",
    ),
):
    """
    Command-line entry point.

    Loads game data, trains the Elo model, and saves the final team ratings.
    """
    try:
        games = load_games(games_path)
        ratings = train_elo_model(games)
        save_ratings(ratings, output_path)
        logging.info("Elo training pipeline completed successfully.")
    except Exception as e:
        logging.error(f"Error in training pipeline: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
