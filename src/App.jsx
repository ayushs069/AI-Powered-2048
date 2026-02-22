import { useState, useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import LoadingScreen from './components/LoadingScreen';
import GameBoard     from './components/GameBoard';
import ControlPanel  from './components/ControlPanel';
import AIControls    from './components/AIControls';
import TipsPanel     from './components/TipsPanel';
import GameOverlay   from './components/GameOverlay';
import { useGameState } from './hooks/useGameState';
import './styles/global.css';

export default function App() {
  const [loading, setLoading] = useState(true);

  const {
    state,
    aiMode, aiSpeed,
    setAiMode, setAiSpeed,
    newGame, move, undo, keepPlaying,
    onTouchStart, onTouchEnd,
  } = useGameState();

  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 2600);
    return () => clearTimeout(t);
  }, []);

  return (
    <>
      <AnimatePresence>
        {loading && <LoadingScreen key="loading" onDone={() => setLoading(false)} />}
      </AnimatePresence>

      {!loading && (
        <motion.div
          className="app"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55, ease: 'easeOut' }}
        >
          {/* Ambient blobs */}
          <div className="blob blob-top-left" />
          <div className="blob blob-bottom-right" />
          <div className="blob blob-mid" />

          <div className="layout">
            {/* ── Left sidebar ── */}
            <aside className="sidebar sidebar-left">
              <ControlPanel
                state={state}
                onNewGame={newGame}
                onUndo={undo}
                onKeepPlaying={keepPlaying}
              />
              <TipsPanel />
            </aside>

            {/* ── Center board ── */}
            <main className="center">
              <div className="brand">
                <h1 className="brand-title">
                  AI <span className="brand-accent">2048</span>
                </h1>
                <p className="brand-sub">Slide tiles · Reach 2048 · Beat the AI</p>
              </div>

              {/* Board + overlay wrapper */}
              <div className="board-outer">
                <GameBoard
                  state={state}
                  move={move}
                  onTouchStart={onTouchStart}
                  onTouchEnd={onTouchEnd}
                />

                {/* Full-screen overlay centered over board */}
                <AnimatePresence>
                  {(state.won || state.lost) && (
                    <GameOverlay
                      key={state.won ? 'won' : 'lost'}
                      won={state.won}
                      lost={state.lost}
                      score={state.score}
                      onKeepPlaying={state.won ? keepPlaying : null}
                      onNewGame={() => newGame(state.difficulty)}
                    />
                  )}
                </AnimatePresence>
              </div>
            </main>

            {/* ── Right sidebar ── */}
            <aside className="sidebar sidebar-right">
              <AIControls
                aiMode={aiMode}
                aiSpeed={aiSpeed}
                onSetMode={setAiMode}
                onSetSpeed={setAiSpeed}
              />
            </aside>
          </div>
        </motion.div>
      )}
    </>
  );
}
