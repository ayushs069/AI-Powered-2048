// ============================================================
// GAME LOGIC — Board state, moves, difficulty, undo
// ============================================================

export const BOARD_SIZE = 4;

/**
 * Create a fresh empty 4×4 grid with two starting tiles.
 */
export function createInitialBoard(difficulty = 'medium') {
  const grid = Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(0));
  const state = { grid, score: 0, history: [], bestScore: 0, difficulty };
  return spawnTile(spawnTile(state));
}

// ── Tile spawning ────────────────────────────────────────────

function getSpawnValue(grid, difficulty) {
  const maxTile = Math.max(...grid.flat());

  if (difficulty === 'easy') {
    if (maxTile >= 1024) return weightedRandom([64, 128, 256, 512], [10, 20, 30, 40]);
    if (maxTile >= 512)  return weightedRandom([32, 64, 128, 256], [15, 25, 35, 25]);
    if (maxTile >= 256)  return weightedRandom([16, 32, 64, 128],  [20, 30, 35, 15]);
    if (maxTile >= 128)  return weightedRandom([8, 16, 32, 64],    [20, 30, 35, 15]);
    if (maxTile >= 64)   return weightedRandom([8, 16, 32],        [30, 40, 30]);
    if (maxTile >= 32)   return weightedRandom([4, 8, 16],         [30, 45, 25]);
    if (maxTile >= 16)   return weightedRandom([4, 8],             [50, 50]);
    return weightedRandom([2, 4], [40, 60]);
  }

  if (difficulty === 'hard') {
    return weightedRandom([2, 4], [90, 10]);
  }

  // medium
  if (maxTile >= 512) return weightedRandom([4, 8, 16, 32],  [35, 35, 20, 10]);
  if (maxTile >= 256) return weightedRandom([4, 8, 16],       [40, 40, 20]);
  if (maxTile >= 128) return weightedRandom([4, 8, 16],       [45, 40, 15]);
  if (maxTile >= 64)  return weightedRandom([4, 8, 16],       [50, 35, 15]);
  if (maxTile >= 32)  return weightedRandom([2, 4, 8],        [55, 35, 10]);
  return weightedRandom([2, 4], [70, 30]);
}

function weightedRandom(values, weights) {
  const total = weights.reduce((a, b) => a + b, 0);
  let r = Math.random() * total;
  for (let i = 0; i < values.length; i++) {
    r -= weights[i];
    if (r <= 0) return values[i];
  }
  return values[values.length - 1];
}

export function spawnTile(state) {
  const empty = getEmptyCells(state.grid);
  if (empty.length === 0) return state;
  const [r, c] = empty[Math.floor(Math.random() * empty.length)];
  const value = getSpawnValue(state.grid, state.difficulty);
  const newGrid = state.grid.map(row => [...row]);
  newGrid[r][c] = value;
  return { ...state, grid: newGrid, lastSpawned: { r, c, value, id: Date.now() + Math.random() } };
}

// ── Helpers ──────────────────────────────────────────────────

export function getEmptyCells(grid) {
  const cells = [];
  for (let r = 0; r < BOARD_SIZE; r++)
    for (let c = 0; c < BOARD_SIZE; c++)
      if (grid[r][c] === 0) cells.push([r, c]);
  return cells;
}

export function canMove(grid) {
  if (getEmptyCells(grid).length > 0) return true;
  for (let r = 0; r < BOARD_SIZE; r++)
    for (let c = 0; c < BOARD_SIZE; c++) {
      if (c < BOARD_SIZE - 1 && grid[r][c] === grid[r][c + 1]) return true;
      if (r < BOARD_SIZE - 1 && grid[r][c] === grid[r + 1][c]) return true;
    }
  return false;
}

export function hasWon(grid) {
  return grid.some(row => row.some(v => v >= 2048));
}

// ── Single-row merge (move left) ─────────────────────────────

function mergeRow(row) {
  const compressed = row.filter(v => v !== 0);
  const merged = [];
  let gained = 0;
  let i = 0;
  while (i < compressed.length) {
    if (i < compressed.length - 1 && compressed[i] === compressed[i + 1]) {
      const val = compressed[i] * 2;
      merged.push(val);
      gained += val;
      i += 2;
    } else {
      merged.push(compressed[i]);
      i++;
    }
  }
  while (merged.length < BOARD_SIZE) merged.push(0);
  return { row: merged, gained };
}

// ── Apply move ───────────────────────────────────────────────

/**
 * Returns { grid, scoreDelta } without spawning a tile.
 * Returns null if no tile moved.
 */
export function applyMove(grid, direction) {
  let rotated = rotateTo(grid, direction);
  let totalGain = 0;
  let changed = false;
  const newGrid = rotated.map(row => {
    const { row: merged, gained } = mergeRow(row);
    totalGain += gained;
    if (!arraysEqual(merged, row)) changed = true;
    return merged;
  });
  if (!changed) return null;
  return { grid: rotateFrom(newGrid, direction), scoreDelta: totalGain };
}

// Rotate grid so that the target direction becomes "left"
function rotateTo(grid, direction) {
  if (direction === 'left')  return grid.map(row => [...row]);
  if (direction === 'right') return grid.map(row => [...row].reverse());
  if (direction === 'up')    return transpose(grid);
  if (direction === 'down')  return transpose(grid).map(row => [...row].reverse());
  return grid;
}

function rotateFrom(grid, direction) {
  if (direction === 'left')  return grid;
  if (direction === 'right') return grid.map(row => [...row].reverse());
  if (direction === 'up')    return transpose(grid);
  if (direction === 'down')  return transpose(grid.map(row => [...row].reverse()));
  return grid;
}

function transpose(grid) {
  return grid[0].map((_, c) => grid.map(row => row[c]));
}

function arraysEqual(a, b) {
  return a.every((v, i) => v === b[i]);
}

// ── Public move handler ───────────────────────────────────────

export function makeMove(state, direction) {
  const result = applyMove(state.grid, direction);
  if (!result) return state;

  const newScore = state.score + result.scoreDelta;
  const newHistory = [...state.history, { grid: state.grid, score: state.score }].slice(-5);

  const afterSpawn = spawnTile({
    ...state,
    grid: result.grid,
    score: newScore,
    history: newHistory,
    bestScore: Math.max(state.bestScore, newScore),
  });

  return afterSpawn;
}

// ── Undo ──────────────────────────────────────────────────────

export function undoMove(state) {
  if (state.history.length === 0) return state;
  const history = [...state.history];
  const last = history.pop();
  return { ...state, grid: last.grid, score: last.score, history };
}

// ── Clone for AI ─────────────────────────────────────────────

export function cloneState(state) {
  return {
    grid: state.grid.map(row => [...row]),
    score: state.score,
    history: [],
    bestScore: state.bestScore,
    difficulty: state.difficulty,
  };
}
