# NFL Super Bowl Predictor 🏈

This project predicts the probability of each NFL team winning the Super Bowl using an Elo rating model and simulated playoff brackets.

## How It Works
1. `src/train.py` processes `data/games.csv` and generates updated Elo ratings.
2. `src/simulate_playoffs.py` uses the Elo model to simulate thousands of playoff outcomes.
3. The simulation results are saved in `outputs/sb_probs_<season>.csv`.

---

## File Structure

