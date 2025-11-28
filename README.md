# 🎮 Futuristic 2048 (Enhanced, Easy-to-Win)

A polished 2048 game with a modern glassmorphic UI, adaptive spawning to help you reach 2048, two AI agents (Greedy and Expectimax), undo, and a professional control panel.

---

## ✨ What’s Included (Only features used)

- Glassmorphic/Neumorphic UI with animated background and particles
- Adaptive tile spawning with Easy/Medium/Hard difficulty
- Two AI agents: Greedy and Expectimax (depth configurable)
- Heuristic visualization (empty tiles, smoothness, monotonicity, corner)
- Undo (up to 5 moves)
- Control panel with speed mode and difficulty toggles
- Larger fonts, improved contrast, fixed tile visibility (1024 uses black text)
- Victory overlay when you reach 2048 (dismiss with any key)
- Persistent best score

Not included: auto-solve, heatmap, MCTS, extra markdown docs.

---

## 🚀 Quick Start

- Install dependencies:
  - pip install -r requirements.txt
- Run the game:
  - python futuristic_complete_2048.py
  - Or double-click run_game.bat on Windows

---

## 🎮 Controls (Only keys implemented)

- Arrow Keys: Move tiles
- A: Toggle AI mode on/off
- M: Switch agent (Human ↔ Greedy ↔ Expectimax)
- R: Reset game
- U: Undo last move (max 5)
- F: Cycle speed mode (Normal, Fast, Instant)
- D: Cycle difficulty (Easy, Medium, Hard)
- + / -: Increase/decrease Expectimax depth
- ESC: Quit

---

## 🏆 Easy Mode Strategy

Adaptive spawning helps you win:
- Early: more 2/4/8 tiles
- Mid: 16/32/64 appear more often
- Late (≥128/256/512): generous high tiles
- Near victory (≥1024): frequent 256/512 spawns

Tips:
- Keep your highest tile locked in a corner
- Favor two directions (e.g., Right and Down)
- Maintain empty spaces and build descending chains

---

## 🤖 AI (Implemented)

- Greedy: Chooses the move with the highest immediate heuristic score
- Expectimax: Depth-limited game tree with chance nodes (2/4 spawns) and heuristic evaluation
- Heuristics used:
  - Empty tiles (more space)
  - Smoothness (neighbor similarity via log2)
  - Monotonicity (ordered rows/columns)
  - Corner bonus (max tile in a corner)

---

## 📂 Project Files

- futuristic_complete_2048.py — Main game (UI, logic, AI, controls)
- README.md — This document
- requirements.txt — pygame, numpy
- run_game.bat — Windows launcher
- best_score.json — Saved high score
- benchmark_results.json — Reserved for benchmarking output

---

## 🛠️ Technical Notes (Used in code)

- Board: 4×4 matrix, row/column transforms for moves (transpose/reverse)
- Adaptive spawning per difficulty (random.choices with weights)
- Undo via move_history stack
- Tile rendering with glow for high values, dynamic text color
- Animation system for spawn/merge; particle bursts for feedback
- Control panel: AI state, agent, depth, speed mode, difficulty
- Victory detection (≥2048) with animated overlay

---

## 🐛 Troubleshooting

- Ensure Python ≥ 3.7 and pygame installed
- If performance lags, use Normal speed, reduce Expectimax depth
- If audio issues occur, sound calls are safe no-ops

---

## 📜 License & Credits

- Built with Pygame and NumPy