import { motion } from 'framer-motion';

const DIFFICULTIES = ['easy', 'medium', 'hard'];

const DIFF_META = {
  easy:   { color: '#22c55e', glow: 'rgba(34,197,94,0.3)',   label: 'Easy'   },
  medium: { color: '#f59e0b', glow: 'rgba(245,158,11,0.3)',  label: 'Medium' },
  hard:   { color: '#ef4444', glow: 'rgba(239,68,68,0.3)',   label: 'Hard'   },
};

export default function ControlPanel({ state, onNewGame, onUndo, onKeepPlaying }) {
  const { score, bestScore, difficulty } = state;

  return (
    <div className="control-panel">

      {/* Score row */}
      <div className="score-row">
        <ScoreBox label="SCORE" value={score} />
        <ScoreBox label="BEST"  value={bestScore} accent />
      </div>

      {/* Difficulty tabs */}
      <div className="difficulty-row">
        {DIFFICULTIES.map(d => {
          const meta = DIFF_META[d];
          const isActive = d === difficulty;
          return (
            <motion.button
              key={d}
              className={`diff-btn ${isActive ? 'active' : ''}`}
              style={isActive ? {
                '--diff-color': meta.color,
                '--diff-glow':  meta.glow,
              } : {}}
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.96 }}
              onClick={() => onNewGame(d)}
            >
              {meta.label}
            </motion.button>
          );
        })}
      </div>

      {/* Action buttons */}
      <div className="action-row">
        <ActionButton label="New Game" icon="⟳" onClick={() => onNewGame(difficulty)} primary />
        <ActionButton label="Undo"     icon="↩" onClick={onUndo} disabled={!state.history?.length} />
      </div>

    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────

function ScoreBox({ label, value, accent }) {
  return (
    <div className={`score-box ${accent ? 'score-box--accent' : ''}`}>
      <span className="score-label">{label}</span>
      <motion.span
        className="score-value"
        key={value}
        initial={{ scale: 1.25, opacity: 0.5 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.22 }}
      >
        {value.toLocaleString()}
      </motion.span>
    </div>
  );
}

function ActionButton({ label, icon, onClick, primary, disabled }) {
  return (
    <motion.button
      className={`action-btn ${primary ? 'action-btn--primary' : ''}`}
      onClick={onClick}
      disabled={disabled}
      whileHover={!disabled ? { scale: 1.03 } : {}}
      whileTap={!disabled ? { scale: 0.97 } : {}}
    >
      <span className="btn-icon">{icon}</span>
      {label}
    </motion.button>
  );
}
