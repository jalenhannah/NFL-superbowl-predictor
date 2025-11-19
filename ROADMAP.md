# Project Roadmap — NFL Super Bowl Predictor

This roadmap tracks planned tasks, completed work, and new tasks discovered during Sprint 2.

---

## Sprint 2 Progress (Updated)

### ✔ Completed Work
- [x] Refactored `train.py` into clean functions with docstrings and comments
- [x] Fixed CSV column names to match `games.csv` (`home`, `away`, `home_pts`, `away_pts`)
- [x] Implemented Elo-based win probability logic in `simulate_game()`
- [x] Added full elimination-bracket logic in `simulate_bracket()`
- [x] Updated README.md with installation instructions, usage examples, and project overview

---

##  In Progress
- [ ] Add visualization script to graph Super Bowl win probabilities
- [ ] Improve input validation for playoff brackets
- [ ] Add command-line options for choosing bracket size or custom seeds

---

## ➕ Emerging Tasks (Added During Sprint 2)
- [ ] Add a configuration file for setting number of simulations, k-factor, and home advantage
- [ ] Create unit tests for EloModel to verify update behavior
- [ ] Allow logging levels to be adjusted (INFO → DEBUG)
- [ ] Add support for saving simulation outputs with timestamps

---

## Sprint Goal
Produce a fully functioning Elo-based NFL playoff simulator that:
- Trains Elo ratings from real historical data  
- Simulates thousands of playoff b

