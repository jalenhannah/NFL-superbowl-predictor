"""
visualize_probs.py

Generate a bar chart showing Super Bowl win probabilities for each team.
Reads the output from simulate_playoffs.py (sb_probs.csv or similar).
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_probabilities(path: Path) -> pd.DataFrame:
    """
    Load Super Bowl win probabilities from CSV.

    Args:
        path: Path to the sb_probs CSV file.

    Returns:
        DataFrame with team and sb_win_prob columns.
    """
    if not path.exists():
        raise FileNotFoundError(f"Probability file not found at {path}")
    
    df = pd.read_csv(path)
    return df


def plot_probabilities(df: pd.DataFrame, title: str = "Super Bowl Win Probabilities"):
    """
    Plot a bar chart of Super Bowl win probabilities.

    Args:
        df: DataFrame containing 'team' and 'sb_win_prob'.
        title: Title for the chart.
    """
    df = df.sort_values("sb_win_prob", ascending=False)

    plt.figure(figsize=(12, 6))
    plt.bar(df["team"], df["sb_win_prob"], color="royalblue")
    plt.xlabel("Team")
    plt.ylabel("Win Probability")
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def main():
    """
    Load probabilities and show the bar chart.
    Modify the file path if needed.
    """
    path = Path("outputs/sb_probs_2025.csv")  # Adjust filename if needed
    df = load_probabilities(path)
    plot_probabilities(df)


if __name__ == "__main__":
    main()

