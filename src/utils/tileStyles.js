// Tile value → visual properties
export const TILE_STYLES = {
  0:    { bg: 'rgba(255,255,255,0.026)', text: 'transparent',  glow: 'none' },

  // Low tiles — cool blues / slates
  2:    { bg: 'linear-gradient(135deg,#1e3a5f,#172b49)', text: '#93c5fd', glow: 'rgba(59,130,246,0.35)' },
  4:    { bg: 'linear-gradient(135deg,#1e3a5f,#1a2e50)', text: '#60a5fa', glow: 'rgba(96,165,250,0.4)'  },

  // Mid-low — cyan / teal
  8:    { bg: 'linear-gradient(135deg,#0c3344,#0a2e3d)', text: '#67e8f9', glow: 'rgba(34,211,238,0.45)' },
  16:   { bg: 'linear-gradient(135deg,#0d3d3d,#0a3333)', text: '#5eead4', glow: 'rgba(20,184,166,0.45)' },

  // Mid — emerald / green
  32:   { bg: 'linear-gradient(135deg,#0f3d22,#0c3320)', text: '#6ee7b7', glow: 'rgba(52,211,153,0.45)' },
  64:   { bg: 'linear-gradient(135deg,#14532d,#166534)', text: '#86efac', glow: 'rgba(74,222,128,0.5)'  },

  // Upper-mid — amber / gold
  128:  { bg: 'linear-gradient(135deg,#3d2c00,#4a3500)', text: '#fde68a', glow: 'rgba(251,191,36,0.5)'  },
  256:  { bg: 'linear-gradient(135deg,#44200a,#5a2a0c)', text: '#fcd34d', glow: 'rgba(245,158,11,0.55)' },

  // High — orange / red-orange
  512:  { bg: 'linear-gradient(135deg,#4a1800,#5c2200)', text: '#fdba74', glow: 'rgba(249,115,22,0.55)' },
  1024: { bg: 'linear-gradient(135deg,#4a0a0a,#5c1010)', text: '#fca5a5', glow: 'rgba(239,68,68,0.6)'  },

  // 2048 — prestige violet/fuchsia
  2048: { bg: 'linear-gradient(135deg,#3b0764,#4a1080)', text: '#e879f9', glow: 'rgba(217,70,239,0.7)'  },
};

export function getTileStyle(value) {
  return TILE_STYLES[value] || TILE_STYLES[2048];
}

export function getTileTextSize(value) {
  if (value >= 1024) return '1.35rem';
  if (value >= 128)  return '1.65rem';
  return '2rem';
}
