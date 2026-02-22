import { motion } from 'framer-motion';

export default function GameOverlay({ won, lost, score, onKeepPlaying, onNewGame }) {
  const isWin = won && !lost;

  return (
    <motion.div
      className={`game-overlay ${isWin ? 'game-overlay--win' : 'game-overlay--lose'}`}
      initial={{ opacity: 0, scale: 0.88, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.92, y: -8 }}
      transition={{ duration: 0.32, ease: [0.22, 1, 0.36, 1] }}
    >
      {/* Glow ring */}
      <div className={`overlay-glow ${isWin ? 'glow-win' : 'glow-lose'}`} />

      {/* Emoji / icon */}
      <motion.div
        className="overlay-emoji"
        initial={{ scale: 0.4, rotate: -15 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ delay: 0.1, duration: 0.4, ease: 'backOut' }}
      >
        {isWin ? '🎉' : '💀'}
      </motion.div>

      {/* Title */}
      <motion.h2
        className="overlay-heading"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15, duration: 0.3 }}
      >
        {isWin ? 'You Won!' : 'Game Over'}
      </motion.h2>

      {/* Sub-text */}
      <motion.p
        className="overlay-message"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.22, duration: 0.3 }}
      >
        {isWin
          ? 'You reached the 2048 tile — impressive!'
          : 'No moves left. Better luck next time!'}
      </motion.p>

      {/* Score pill */}
      <motion.div
        className={`overlay-score-pill ${isWin ? 'pill-win' : 'pill-lose'}`}
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.28, duration: 0.3 }}
      >
        <span className="pill-label">Score</span>
        <span className="pill-value">{score.toLocaleString()}</span>
      </motion.div>

      {/* Buttons */}
      <motion.div
        className="overlay-btn-row"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.3 }}
      >
        {onKeepPlaying && (
          <motion.button
            className="ovr-btn ovr-btn--ghost"
            onClick={onKeepPlaying}
            whileHover={{ scale: 1.04, boxShadow: '0 0 18px rgba(99,102,241,0.3)' }}
            whileTap={{ scale: 0.96 }}
          >
            Keep Playing
          </motion.button>
        )}
        <motion.button
          className={`ovr-btn ${isWin ? 'ovr-btn--win' : 'ovr-btn--lose'}`}
          onClick={onNewGame}
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.96 }}
        >
          ⟳ New Game
        </motion.button>
      </motion.div>
    </motion.div>
  );
}
