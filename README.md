# NFL Super Bowl Predictor 🏈
Baseline Python project using an Elo rating model + simple playoff simulation.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/train.py
python src/simulate_playoffs.py --season 2026 --runs 5000
