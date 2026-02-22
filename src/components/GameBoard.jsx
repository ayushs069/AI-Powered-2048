import { useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Tile from './Tile';
import { BOARD_SIZE } from '../utils/gameLogic';

export default function GameBoard({ state, onTouchStart, onTouchEnd }) {
  const { grid, lastSpawned } = state;

  // Build flat tile list with stable ids
  const tileKeyMap = useRef(new Map());
  const counter    = useRef(0);

  // Assign stable keys per position (refreshed each render)
  const tiles = [];
  for (let r = 0; r < BOARD_SIZE; r++) {
    for (let c = 0; c < BOARD_SIZE; c++) {
      const val = grid[r][c];
      if (val === 0) continue;

      const posKey = `${r}-${c}`;
      if (!tileKeyMap.current.has(posKey)) {
        tileKeyMap.current.set(posKey, ++counter.current);
      }

      const isNew    = lastSpawned && lastSpawned.r === r && lastSpawned.c === c;
      tiles.push({
        id: isNew ? lastSpawned.id : tileKeyMap.current.get(posKey),
        value: val,
        row: r,
        col: c,
        isNew: !!isNew,
        isMerged: false,
      });
    }
  }

  return (
    <div
      className="board-wrapper"
      onTouchStart={onTouchStart}
      onTouchEnd={onTouchEnd}
    >
      {/* Ghost cells (background grid) */}
      <div className="board-grid board-bg">
        {Array.from({ length: BOARD_SIZE * BOARD_SIZE }).map((_, i) => (
          <div key={i} className="cell-ghost" />
        ))}
      </div>

      {/* Live tiles */}
      <div className="board-grid board-tiles">
        <AnimatePresence>
          {tiles.map(t => (
            <Tile key={t.id} {...t} />
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
