import { motion } from 'framer-motion';

export default function LoadingScreen({ onDone }) {
  return (
    <motion.div
      className="loading-screen"
      initial={{ opacity: 1 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.6, ease: 'easeInOut' }}
      onAnimationComplete={() => {
        setTimeout(onDone, 1200);
      }}
    >
      {/* Ambient blobs */}
      <div className="blob blob-1" />
      <div className="blob blob-2" />

      <motion.div
        className="loading-inner"
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: 'easeOut' }}
      >
        {/* Logo grid */}
        <div className="logo-grid">
          {['2', '0', '4', '8'].map((char, i) => (
            <motion.div
              key={i}
              className="logo-tile"
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 + i * 0.1, duration: 0.4, ease: 'backOut' }}
              style={{
                background: ['#1e3a5f','#1d3557','#2d3748','#4a1942'][i],
                color:       ['#bfdbfe','#6ee7f7','#fcd34d','#e879f9'][i],
                boxShadow:   `0 0 18px ${['#3b82f6','#06b6d4','#f59e0b','#d946ef'][i]}55`,
              }}
            >
              {char}
            </motion.div>
          ))}
        </div>

        <motion.h1
          className="loading-title"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.5 }}
        >
          AI <span className="accent">2048</span>
        </motion.h1>

        <motion.p
          className="loading-subtitle"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.75, duration: 0.5 }}
        >
          Powered by Expectimax &amp; Greedy Intelligence
        </motion.p>

        {/* Spinner bar */}
        <motion.div
          className="progress-bar"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.9 }}
        >
          <motion.div
            className="progress-fill"
            initial={{ width: '0%' }}
            animate={{ width: '100%' }}
            transition={{ delay: 1.0, duration: 0.9, ease: 'easeInOut' }}
          />
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
