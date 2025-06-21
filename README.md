# 🧠 Connect Four with Minimax AI

A Python implementation of the classic **Connect Four** game featuring:
- Console-based UI
- Two-player gameplay (Human vs AI)
- AI powered by the **Minimax algorithm with Alpha-Beta pruning**
- Board evaluation heuristics for smarter decision-making

---

## 🎮 Gameplay Overview

- Board size: 6 rows × 5 columns
- Player 1 (Human) uses `"X"`, AI uses `"O"`
- Players take turns dropping pieces into a column
- First to connect **four** pieces in a row — horizontally, vertically, or diagonally — wins
- If the board fills with no winner, it's a **draw**

---

## 🧠 AI Logic

The AI uses the **Minimax algorithm with Alpha-Beta pruning** to determine the best possible move at each turn. It evaluates board states using:
- Winning combinations count
- Center column preference
- Custom heuristics for pattern recognition (e.g. 3 in a row, 2 in a row, etc.)

---

## 🛠️ Features

- `minimax()` for basic AI (first iteration)
- `minimax_alpha_beta()` for optimized AI (second iteration)
- Board evaluation functions:
  - `evaluate_board()`
  - `count_winning_combinations()`
  - `count_patterns()`
- Move undoing to simulate future game states
- Center-out column preference to mimic real-world playstyle

---

## ▶️ How to Run

Make sure you have Python and NumPy installed:

```bash
pip install numpy
python connect_four.py
