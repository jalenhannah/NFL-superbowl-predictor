"""
simulate_playoffs.py

Simulate NFL playoffs using Elo ratings and estimate Super Bowl probabilities.
"""

import logging
from pathlib import Path
import random

import pandas as pd
import typer
from models.elo import EloModel  # uses your EloModel with ratings + home_adv

app = typer.Typer(add_completion=False)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_ratings(path: Path) -> dict:
    """
    Load Elo ratings from CSV into a dict.

    Args:
        path: Path to elo_ratings.csv

    Returns:
        Dict mapping team -> Elo rating.
    """
    if not path.exists():
        raise FileNotFoundError(f"Elo ratings file not found at {path}")

    s = pd.read_csv(path, index_col=0).iloc[:, 0]
    return {team: float(rating) for team, rating in s.items()}


def simulate_game(home_team: str, away_team: str, elo: EloModel) -> str:
    """
    Simulate a single game between two teams using the Elo model's win probability.

    We treat the first team passed in as the home team, and apply the home
    advantage just like EloModel.game() does.

    Args:
        home_team: Name of the home team.
        away_team: Name of the away team.
        elo: EloModel instance containing current team ratings.

    Returns:
        Winner team name.
    """
    # Get current Elo ratings and add home advantage for the home team
    r_home = elo.ratings[home_team] + elo.home_adv
    r_away = elo.ratings[away_team]

    # Use the same win probability formula as EloModel._win_prob
    p_home = EloModel._win_prob(r_home, r_away)

    # Draw a random number to decide the winner
    if random.random() < p_home:
        return home_team
    else:
        return away_team


def simulate_bracket(teams: list[str], elo: EloModel) -> str:
    """
    Simulate a full single-elimination playoff bracket and return the Super Bowl winner.

    Seeding logic:
    - Teams are sorted by Elo rating (highest first)
    - In each round, teams are paired in order (1 vs 2, 3 vs 4, etc.)
    - The first team in each pair is treated as the home team for simulation

    Args:
        teams: List of team names in the playoff.
        elo: EloModel containing Elo ratings for all teams.

    Returns:
        Name of the Super Bowl winner.
    """
    # Sort teams by Elo rating, highest first, to simulate seeding
    sorted_teams = sorted(teams, key=lambda t: elo.ratings[t], reverse=True)
    round_teams = sorted_teams[:]

    # Keep playing rounds until only one team remains
    while len(round_teams) > 1:
        next_round = []

        # If there's an odd number of teams, give the last team a bye
        if len(round_teams) % 2 == 1:
            bye_team = round_teams.pop()  # team with implicit bye
            next_round.append(bye_team)

        # Pair up teams and simulate games
        for i in range(0, len(round_teams), 2):
            home = round_teams[i]
            away = round_teams[i + 1]
            winner = simulate_game(home, away, elo)
            next_round.append(winner)

        round_teams = next_round

    # Last team standing is the simulated Super Bowl winner
    return round_teams[0]


def simulate_season(
    ratings: dict,
    n_sims: int,
    output_path: Path,
):
    """
    Run many playoff simulations and save Super Bowl win probabilities.

    Args:
        ratings: Dict of team -> Elo rating.
        n_sims: Number of simulations to run.
        output_path: CSV path for probability outputs.
    """
    teams = list(ratings.keys())
    if len(teams) == 0:
        logging.error("No teams found in ratings. Exiting.")
        return

    # Initialize EloModel and load the provided ratings into its .ratings dict
    elo = EloModel()
    elo.ratings.update(ratings)

    win_counts = {team: 0 for team in teams}

    logging.info(f"Running {n_sims} playoff simulations...")
    for i in range(n_sims):
        winner = simulate_bracket(teams, elo)
        win_counts[winner] += 1

        if (i + 1) % max(1, n_sims // 10) == 0:
            logging.info(f"Completed {i + 1} simulations...")

    # Convert counts to probabilities
    probs = {team: win_counts[team] / n_sims for team in teams}
    df = pd.DataFrame.from_dict(probs, orient="index", columns=["sb_win_prob"])
    df.index.name = "team"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path)
    logging.info(f"Saved Super Bowl probabilities to {output_path}")


@app.command()
def main(
    ratings_path: Path = typer.Option(
        Path("outputs/elo_ratings.csv"),
        help="Path to the Elo ratings CSV file",
    ),
    n_sims: int = typer.Option(
        10000,
        help="Number of playoff simulations to run",
    ),
    output_path: Path = typer.Option(
        Path("outputs/sb_probs_2025.csv"),
        help="Path to save Super Bowl probabilities CSV",
    ),
):
    """
    Run Elo-based playoff simulations and save Super Bowl probabilities.
    """
    try:
        ratings = load_ratings(ratings_path)
        simulate_season(ratings, n_sims, output_path)
    except Exception as e:
        logging.error(f"Error during simulation: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
