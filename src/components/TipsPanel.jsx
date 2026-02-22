import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const TIPS = [
  {
    icon: '📐',
    color: '#6366f1',
    glow: 'rgba(99,102,241,0.25)',
    title: 'Corner Strategy',
    body: 'Keep your highest tile locked in one corner (top-left or bottom-right). Never move it away from that corner.',
  },
  {
    icon: '📉',
    color: '#06b6d4',
    glow: 'rgba(6,182,212,0.22)',
    title: 'Stay Monotonic',
    body: 'Arrange tiles so values decrease in one direction — e.g. largest → smallest from left to right on every row.',
  },
  {
    icon: '🚫',
    color: '#f59e0b',
    glow: 'rgba(245,158,11,0.22)',
    title: 'Avoid Reversals',
    body: 'Limit moves that go against your chosen corner direction. If your corner is top-left, prioritise ← and ↑.',
  },
  {
    icon: '🔢',
    color: '#22c55e',
    glow: 'rgba(34,197,94,0.22)',
    title: 'Chain Merges',
    body: 'Set up tiles so one move triggers multiple merges at once — this maximises score and saves space.',
  },
  {
    icon: '🧠',
    color: '#d946ef',
    glow: 'rgba(217,70,239,0.22)',
    title: 'Use Expectimax AI',
    body: 'Turn on Expectimax AI to watch optimal play. Study its moves to improve your own strategy.',
  },
  {
    icon: '↩',
    color: '#94a3b8',
    glow: 'rgba(148,163,184,0.18)',
    title: 'Undo Wisely',
    body: 'Use Undo after an accidental move that breaks your corner strategy. You get 5 undos per game.',
  },
];

export default function TipsPanel() {
  const [open, setOpen] = useState(true);
  const [active, setActive] = useState(null);

  return (
    <div className="tips-panel">
      {/* Header — toggles expand */}
      <button className="tips-header" onClick={() => setOpen(o => !o)}>
        <span className="tips-header-left">
          <span className="tips-icon-badge">💡</span>
          <span className="tips-title">Pro Tips</span>
          <span className="tips-count">{TIPS.length}</span>
        </span>
        <motion.span
          className="tips-chevron"
          animate={{ rotate: open ? 180 : 0 }}
          transition={{ duration: 0.22 }}
        >
          ▾
        </motion.span>
      </button>

      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            className="tips-body"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.28, ease: 'easeInOut' }}
          >
            <div className="tips-list">
              {TIPS.map((tip, i) => (
                <TipCard
                  key={i}
                  tip={tip}
                  isOpen={active === i}
                  onToggle={() => setActive(active === i ? null : i)}
                />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function TipCard({ tip, isOpen, onToggle }) {
  return (
    <div
      className={`tip-card ${isOpen ? 'tip-card--open' : ''}`}
      style={{ '--tip-color': tip.color, '--tip-glow': tip.glow }}
      onClick={onToggle}
    >
      <div className="tip-card-header">
        <span className="tip-card-icon">{tip.icon}</span>
        <span className="tip-card-title">{tip.title}</span>
        <motion.span
          className="tip-chevron"
          animate={{ rotate: isOpen ? 90 : 0 }}
          transition={{ duration: 0.18 }}
        >
          ›
        </motion.span>
      </div>

      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.p
            className="tip-card-body"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.22, ease: 'easeInOut' }}
          >
            {tip.body}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}
