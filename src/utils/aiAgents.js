// ============================================================
// AI AGENTS — Greedy & Expectimax
// ============================================================

import { applyMove, cloneState, getEmptyCells, canMove } from './gameLogic';

const DIRECTIONS = ['up', 'down', 'left', 'right'];

// ── Heuristics ────────────────────────────────────────────────

function calcHeuristics(grid) {
  const size = grid.length;

  // 1. Empty cells
  const emptyCount = grid.flat().filter(v => v === 0).length;
  const emptyScore = emptyCount * 10;

  // 2. Smoothness
  let smoothness = 0;
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      if (grid[r][c] !== 0) {
        const val = Math.log2(grid[r][c]);
        if (c < size - 1 && grid[r][c + 1] !== 0)
          smoothness -= Math.abs(val - Math.log2(grid[r][c + 1]));
        if (r < size - 1 && grid[r + 1][c] !== 0)
          smoothness -= Math.abs(val - Math.log2(grid[r + 1][c]));
      }
    }
  }

  // 3. Monotonicity
  let monotonicity = 0;
  for (let r = 0; r < size; r++) {
    let inc = 0, dec = 0;
    for (let c = 0; c < size - 1; c++) {
      if (grid[r][c] !== 0 && grid[r][c + 1] !== 0) {
        const a = Math.log2(grid[r][c]);
        const b = Math.log2(grid[r][c + 1]);
        if (a <= b) inc += b - a; else dec += a - b;
      }
    }
    monotonicity += Math.max(inc, dec);
  }
  for (let c = 0; c < size; c++) {
    let inc = 0, dec = 0;
    for (let r = 0; r < size - 1; r++) {
      if (grid[r][c] !== 0 && grid[r + 1][c] !== 0) {
        const a = Math.log2(grid[r][c]);
        const b = Math.log2(grid[r + 1][c]);
        if (a <= b) inc += b - a; else dec += a - b;
      }
    }
    monotonicity += Math.max(inc, dec);
  }

  // 4. Corner reward
  const maxTile = Math.max(...grid.flat());
  const corners = [[0,0],[0,size-1],[size-1,0],[size-1,size-1]];
  let cornerBonus = 0;
  for (const [r, c] of corners) {
    if (grid[r][c] === maxTile) { cornerBonus = maxTile * 2; break; }
  }

  return emptyScore * 0.25 + smoothness * 0.25 + monotonicity * 0.25 + cornerBonus * 0.25;
}

// ── Greedy agent ──────────────────────────────────────────────

export function greedyAgent(state) {
  let bestMove = null;
  let bestScore = -Infinity;

  for (const dir of DIRECTIONS) {
    const result = applyMove(state.grid, dir);
    if (!result) continue;
    const score = calcHeuristics(result.grid);
    if (score > bestScore) { bestScore = score; bestMove = dir; }
  }
  return bestMove;
}

// ── Expectimax agent ──────────────────────────────────────────

function expectimax(grid, depth, isPlayer) {
  if (depth === 0 || !canMove(grid)) return calcHeuristics(grid);

  if (isPlayer) {
    let max = -Infinity;
    for (const dir of DIRECTIONS) {
      const result = applyMove(grid, dir);
      if (!result) continue;
      const val = expectimax(result.grid, depth - 1, false);
      if (val > max) max = val;
    }
    return max === -Infinity ? 0 : max;
  } else {
    // Chance node: average over all empty cells × {2, 4}
    const empties = getEmptyCells(grid);
    if (empties.length === 0) return calcHeuristics(grid);

    let expected = 0;
    for (const [r, c] of empties) {
      const g2 = grid.map(row => [...row]); g2[r][c] = 2;
      const g4 = grid.map(row => [...row]); g4[r][c] = 4;
      expected += (0.9 * expectimax(g2, depth - 1, true) +
                   0.1 * expectimax(g4, depth - 1, true)) / empties.length;
    }
    return expected;
  }
}

export function expectimaxAgent(state, depth = 3) {
  let bestMove = null;
  let bestScore = -Infinity;

  for (const dir of DIRECTIONS) {
    const result = applyMove(state.grid, dir);
    if (!result) continue;
    const score = expectimax(result.grid, depth - 1, false);
    if (score > bestScore) { bestScore = score; bestMove = dir; }
  }
  return bestMove;
}
