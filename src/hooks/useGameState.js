import { useCallback, useEffect, useReducer, useRef, useState } from 'react';
import {
  createInitialBoard,
  makeMove,
  undoMove,
  canMove,
  hasWon,
} from '../utils/gameLogic';
import { greedyAgent, expectimaxAgent } from '../utils/aiAgents';

// ── Reducer ───────────────────────────────────────────────────

function gameReducer(state, action) {
  switch (action.type) {
    case 'NEW_GAME':
      return {
        ...createInitialBoard(action.difficulty),
        bestScore: state.bestScore,
        won: false,
        lost: false,
        keepPlaying: false,
        difficulty: action.difficulty,
      };
    case 'MOVE': {
      if (state.lost || (state.won && !state.keepPlaying)) return state;
      const next = makeMove(state, action.direction);
      if (next === state) return state;
      const won = hasWon(next.grid);
      const lost = !canMove(next.grid);
      return {
        ...next,
        won: won && !state.keepPlaying ? true : state.won,
        lost,
        bestScore: Math.max(next.bestScore, next.score),
      };
    }
    case 'UNDO':
      return { ...undoMove(state), won: false, lost: false };
    case 'KEEP_PLAYING':
      return { ...state, won: false, keepPlaying: true };
    default:
      return state;
  }
}

function init(difficulty) {
  const saved = localStorage.getItem('2048-best');
  const bestScore = saved ? parseInt(saved, 10) : 0;
  return {
    ...createInitialBoard(difficulty),
    bestScore,
    won: false,
    lost: false,
    keepPlaying: false,
    difficulty,
  };
}

// ── Hook ──────────────────────────────────────────────────────

export function useGameState() {
  const [state, dispatch] = useReducer(gameReducer, 'medium', init);
  const [aiMode, setAiMode]         = useState(false);   // false | 'greedy' | 'expectimax'
  const [aiSpeed, setAiSpeed]       = useState(300);     // ms between AI moves
  const aiIntervalRef               = useRef(null);
  const isAnimatingRef              = useRef(false);

  // Persist best score
  useEffect(() => {
    localStorage.setItem('2048-best', String(state.bestScore));
  }, [state.bestScore]);

  // Keyboard handler
  const handleKey = useCallback(
    (e) => {
      if (aiMode) return;
      const map = {
        ArrowUp:    'up',
        ArrowDown:  'down',
        ArrowLeft:  'left',
        ArrowRight: 'right',
        w: 'up', s: 'down', a: 'left', d: 'right',
        W: 'up', S: 'down', A: 'left', D: 'right',
      };
      const dir = map[e.key];
      if (!dir) return;
      e.preventDefault();
      dispatch({ type: 'MOVE', direction: dir });
    },
    [aiMode]
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [handleKey]);

  // AI loop
  useEffect(() => {
    if (aiIntervalRef.current) clearInterval(aiIntervalRef.current);
    if (!aiMode || state.lost || (state.won && !state.keepPlaying)) return;

    aiIntervalRef.current = setInterval(() => {
      if (isAnimatingRef.current) return;
      const move =
        aiMode === 'expectimax'
          ? expectimaxAgent(state, 3)
          : greedyAgent(state);
      if (move) dispatch({ type: 'MOVE', direction: move });
    }, aiSpeed);

    return () => clearInterval(aiIntervalRef.current);
  }, [aiMode, state, aiSpeed]);

  const newGame    = useCallback((diff) => dispatch({ type: 'NEW_GAME', difficulty: diff || state.difficulty }), [state.difficulty]);
  const move       = useCallback((dir)  => dispatch({ type: 'MOVE', direction: dir }),  []);
  const undo       = useCallback(()     => dispatch({ type: 'UNDO' }),                  []);
  const keepPlaying = useCallback(()    => dispatch({ type: 'KEEP_PLAYING' }),           []);

  // Swipe support
  const touchStart = useRef(null);

  const onTouchStart = useCallback((e) => {
    touchStart.current = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  }, []);

  const onTouchEnd = useCallback(
    (e) => {
      if (!touchStart.current) return;
      const dx = e.changedTouches[0].clientX - touchStart.current.x;
      const dy = e.changedTouches[0].clientY - touchStart.current.y;
      const abs = { x: Math.abs(dx), y: Math.abs(dy) };
      if (Math.max(abs.x, abs.y) < 30) return;
      if (abs.x > abs.y) move(dx > 0 ? 'right' : 'left');
      else               move(dy > 0 ? 'down'  : 'up');
      touchStart.current = null;
    },
    [move]
  );

  return {
    state,
    aiMode,
    aiSpeed,
    setAiMode,
    setAiSpeed,
    newGame,
    move,
    undo,
    keepPlaying,
    onTouchStart,
    onTouchEnd,
    isAnimatingRef,
  };
}
