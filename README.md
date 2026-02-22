# 🎮 AI-Powered 2048

A **modern, fully-featured 2048 game** built with React, featuring multiple AI agents, smooth animations, glassmorphic UI, and pro tips — playable entirely in the browser.

![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite)
![Framer Motion](https://img.shields.io/badge/Framer_Motion-11-FF0055?style=flat-square&logo=framer)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

### 🕹️ Core Game
- Classic **4×4 2048 gameplay** — slide tiles, merge numbers, reach 2048!
- Full **keyboard support** (Arrow keys / WASD)
- **Swipe gestures** for touch/mobile devices
- **Undo** last move (limited uses per game)
- **Score tracking** with best score persistence via `localStorage`
- **New Game** button with instant reset

### 🤖 AI Agents
Four distinct AI strategies you can watch play in real time:

| Agent | Strategy |
|-------|----------|
| **Random** | Makes completely random valid moves |
| **Greedy** | Picks the move that scores the most points immediately |
| **Corner** | Keeps the highest tile in a corner using a weighted heuristic |
| **Expectimax** | Looks ahead using expectimax search for optimal play |

- Adjustable **AI speed** (Slow → Blazing Fast)
- Start / Stop AI at any time
- Watch AI score counter update live

### 🎨 UI / UX
- **Glassmorphic design** — frosted glass cards, glowing accents
- **Smooth tile animations** using Framer Motion (spawn, merge, slide)
- **Full-screen Game Over / Victory overlay** with restart prompt
- Responsive layout — works on desktop, tablet, and mobile
- **Difficulty modes**: Easy (5×5), Normal (4×4), Hard (3×3)
- Collapsible **Pro Tips** sidebar panel

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | [React 18](https://react.dev/) |
| Build Tool | [Vite 5](https://vitejs.dev/) |
| Animations | [Framer Motion 11](https://www.framer.com/motion/) |
| Styling | Pure CSS (glassmorphism, CSS variables, grid layout) |
| State | `useReducer` + custom hooks |
| AI Logic | Vanilla JS (Expectimax, heuristics) |

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) v18 or higher
- npm v9 or higher

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/AI-Powered-2048.git
cd AI-Powered-2048

# 2. Navigate to the React app
cd 2048-react

# 3. Install dependencies
npm install

# 4. Start the development server
npm run dev
```

Then open **http://localhost:5173** in your browser.

### Build for Production

```bash
cd 2048-react
npm run build       # Outputs to 2048-react/dist/
npm run preview     # Preview the production build locally
```

---

## 📁 Project Structure

```
AI-Powered-2048/
├── 2048-react/                  # React application
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── AIControls.jsx   # AI agent selector & speed control
│   │   │   ├── ControlPanel.jsx # New game, undo, difficulty, score
│   │   │   ├── GameBoard.jsx    # Main board grid
│   │   │   ├── GameOverlay.jsx  # Game over / victory overlay
│   │   │   ├── LoadingScreen.jsx
│   │   │   ├── Tile.jsx         # Animated individual tile
│   │   │   └── TipsPanel.jsx    # Collapsible pro tips sidebar
│   │   ├── hooks/
│   │   │   └── useGame.js       # Core game state & reducer
│   │   ├── utils/
│   │   │   ├── aiAgents.js      # All four AI agent implementations
│   │   │   ├── gameLogic.js     # Board logic (slide, merge, spawn)
│   │   │   └── tileStyles.js    # Tile color/gradient map
│   │   ├── styles/
│   │   │   └── global.css       # Global CSS with design tokens
│   │   ├── App.jsx              # Root layout component
│   │   └── main.jsx             # React entry point
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── .gitignore
└── README.md
```

---

## 🎯 How to Play

1. **Arrow keys / WASD** — slide all tiles in that direction
2. Tiles with the **same number merge** when they collide, doubling their value
3. Every move spawns a new **2** or **4** tile
4. Reach the **2048 tile** to win — keep going for a high score!
5. The game ends when **no moves remain**

### AI Mode
1. Select an AI agent from the right panel (Random / Greedy / Corner / Expectimax)
2. Adjust the speed slider
3. Press **▶ Start AI** and watch it play

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ and React</p>
