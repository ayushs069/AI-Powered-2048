import { motion, AnimatePresence } from 'framer-motion';
import { getTileStyle, getTileTextSize } from '../utils/tileStyles';

// Stable key map so tiles animate to their new positions
export default function Tile({ value, row, col, id, isNew, isMerged }) {
  const style = getTileStyle(value);
  const fontSize = getTileTextSize(value);

  if (value === 0) return null;

  return (
    <AnimatePresence>
      <motion.div
        key={id}
        className="tile"
        layoutId={String(id)}
        initial={
          isNew
            ? { scale: 0.35, opacity: 0 }
            : isMerged
            ? { scale: 1.18 }
            : { scale: 1, opacity: 1 }
        }
        animate={{ scale: 1, opacity: 1 }}
        transition={{
          duration: isNew ? 0.22 : isMerged ? 0.18 : 0.15,
          ease: 'easeOut',
        }}
        style={{
          background: style.bg,
          color: style.text,
          fontSize,
          '--tile-glow': style.glow,
          gridRow: row + 1,
          gridColumn: col + 1,
        }}
      >
        {value}
      </motion.div>
    </AnimatePresence>
  );
}
