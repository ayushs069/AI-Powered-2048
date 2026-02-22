import { motion } from 'framer-motion';

const AI_MODES = [
  { value: false,        label: 'Off',        icon: '🎮' },
  { value: 'greedy',     label: 'Greedy',     icon: '⚡' },
  { value: 'expectimax', label: 'Expectimax', icon: '🧠' },
];

const SPEEDS = [
  { value: 600, label: 'Slow' },
  { value: 300, label: 'Medium' },
  { value: 120, label: 'Fast' },
];

export default function AIControls({ aiMode, aiSpeed, onSetMode, onSetSpeed }) {
  return (
    <div className="ai-controls">
      <div className="ai-header">
        <span className="ai-icon">🤖</span>
        <span className="ai-label">AI Agent</span>
        {aiMode && <span className="ai-badge">{aiMode === 'expectimax' ? 'Expectimax' : 'Greedy'}</span>}
      </div>

      {/* Mode selector */}
      <div className="ai-mode-row">
        {AI_MODES.map(m => (
          <motion.button
            key={String(m.value)}
            className={`ai-mode-btn ${aiMode === m.value ? 'active' : ''}`}
            onClick={() => onSetMode(m.value)}
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.95 }}
          >
            <span>{m.icon}</span>
            <span>{m.label}</span>
          </motion.button>
        ))}
      </div>

      {/* Speed selector — only visible when AI is on */}
      {aiMode && (
        <motion.div
          className="ai-speed-row"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          transition={{ duration: 0.2 }}
        >
          <span className="speed-label">Speed</span>
          <div className="speed-btns">
            {SPEEDS.map(s => (
              <motion.button
                key={s.value}
                className={`speed-btn ${aiSpeed === s.value ? 'active' : ''}`}
                onClick={() => onSetSpeed(s.value)}
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.96 }}
              >
                {s.label}
              </motion.button>
            ))}
          </div>
        </motion.div>
      )}

      {/* Indicator dot */}
      <div className="ai-status">
        <span className={`status-dot ${aiMode ? 'on' : ''}`} />
        <span className="status-text">
          {aiMode ? `AI running (${aiMode})` : 'Manual control'}
        </span>
      </div>

      {/* Keyboard hint */}
      <div className="key-hints">
        <span className="hint-title">Keyboard</span>
        <div className="hint-keys">
          {['↑','↓','←','→'].map(k => (
            <kbd key={k} className="kbd">{k}</kbd>
          ))}
          <span className="hint-or">or</span>
          {['W','A','S','D'].map(k => (
            <kbd key={k} className="kbd">{k}</kbd>
          ))}
        </div>
      </div>
    </div>
  );
}
