# futuristic_complete_2048.py - Complete Futuristic 2048 Game
"""
🚀 Futuristic 2048 Game with AI & DM Integration
==============================================

A complete implementation of 2048 with advanced features:
- Neumorphic/Glassmorphic UI design
- Smooth animations with particle effects
- AI agents (Greedy & Expectimax)
- Real-time heuristic visualization
- Professional control panel
- Performance optimizations

Discrete Mathematics Concepts:
- Matrix operations for board state
- Graph theory for state transitions
- Combinatorics for move calculations
- Probability distributions for tile spawning

Artificial Intelligence Concepts:
- Heuristic evaluation functions
- Expectimax algorithm with chance nodes
- Monte Carlo methods
- Game tree search
"""

import pygame
import pygame.gfxdraw as gfx
import math
import random
import time
import json
import numpy as np
from typing import List, Tuple, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import os

# ========================================
# GAME CONSTANTS & CONFIGURATION
# ========================================

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
BOARD_SIZE = 4
CELL_SIZE = 120
MARGIN = 20

# Futuristic Color Palette
COLORS = {
    'background_start': (15, 23, 42),    # Dark navy
    'background_end': (0, 0, 0),        # Black
    'neon_cyan': (0, 255, 255),
    'neon_magenta': (255, 0, 255),
    'electric_orange': (255, 165, 0),
    'lime_green': (50, 205, 50),
    'deep_pink': (255, 20, 147),
    'blue_violet': (138, 43, 226),
    'gold': (255, 215, 0),
    'red_orange': (255, 69, 0),
    'deep_sky_blue': (0, 191, 255),
    'pure_white': (255, 255, 255),
    'panel_bg': (25, 35, 55, 160),       # Increased opacity for better visibility
    'panel_border': (120, 220, 255, 120)  # Brighter border
}

# Tile color mapping for different values
TILE_COLORS = {
    0: (45, 55, 72),        # Empty - dark gray
    2: COLORS['neon_cyan'],
    4: COLORS['neon_magenta'],
    8: COLORS['electric_orange'],
    16: COLORS['lime_green'],
    32: COLORS['deep_pink'],
    64: COLORS['blue_violet'],
    128: COLORS['gold'],
    256: COLORS['red_orange'],
    512: COLORS['deep_sky_blue'],
    1024: COLORS['pure_white'],
    2048: COLORS['gold'],
}

# ========================================
# DISCRETE MATHEMATICS: BOARD MATRIX
# ========================================

class Board:
    """
    Board class implementing discrete mathematics concepts:
    - Matrix representation of game state
    - Matrix operations for tile movements
    - Combinatorial analysis of valid moves
    """
    
    def __init__(self, size: int = 4, difficulty: str = "Medium"):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.score = 0
        self.move_history = []  # Stack for undo functionality
        self.difficulty = difficulty  # Easy, Medium, or Hard
        self.spawn_new_tile()
        self.spawn_new_tile()
    
    def spawn_new_tile(self):
        """Spawn new tile using adaptive probability (DM: Probability Theory + Game Balance)"""
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            
            # Difficulty-based spawning
            if self.difficulty == "Easy":
                # Easy: ULTRA EASY MODE - GUARANTEED 2048! Super high tiles to help you win!
                max_tile = max(max(row) for row in self.grid)
                if max_tile >= 1024:
                    # ONE STEP FROM 2048! Spawn extremely high values - mostly 512s!
                    spawn_value = random.choices([64, 128, 256, 512], weights=[10, 20, 30, 40])[0]
                elif max_tile >= 512:
                    # Getting really close! Spawn tons of high tiles
                    spawn_value = random.choices([32, 64, 128, 256], weights=[15, 25, 35, 25])[0]
                elif max_tile >= 256:
                    # Halfway there! Give lots of help
                    spawn_value = random.choices([16, 32, 64, 128], weights=[20, 30, 35, 15])[0]
                elif max_tile >= 128:
                    # Good progress! Keep giving high tiles
                    spawn_value = random.choices([8, 16, 32, 64], weights=[20, 30, 35, 15])[0]
                elif max_tile >= 64:
                    # Building up! Give good tiles
                    spawn_value = random.choices([8, 16, 32], weights=[30, 40, 30])[0]
                elif max_tile >= 32:
                    # Starting strong!
                    spawn_value = random.choices([4, 8, 16], weights=[30, 45, 25])[0]
                elif max_tile >= 16:
                    # Early game boost
                    spawn_value = random.choices([4, 8], weights=[50, 50])[0]
                else:
                    # Very start - still helpful
                    spawn_value = random.choices([2, 4], weights=[40, 60])[0]
            
            elif self.difficulty == "Hard":
                # Hard: Classic 2048 - only 2s and 4s, 90/10 split
                spawn_value = random.choices([2, 4], weights=[90, 10])[0]
            
            else:  # Medium (default)
                # Medium: Balanced adaptive spawning - generous after 64
                max_tile = max(max(row) for row in self.grid)
                if max_tile >= 512:
                    spawn_value = random.choices([4, 8, 16, 32], weights=[35, 35, 20, 10])[0]
                elif max_tile >= 256:
                    spawn_value = random.choices([4, 8, 16], weights=[40, 40, 20])[0]
                elif max_tile >= 128:
                    spawn_value = random.choices([4, 8, 16], weights=[45, 40, 15])[0]
                elif max_tile >= 64:
                    spawn_value = random.choices([4, 8, 16], weights=[50, 35, 15])[0]
                elif max_tile >= 32:
                    spawn_value = random.choices([2, 4, 8], weights=[55, 35, 10])[0]
                else:
                    spawn_value = random.choices([2, 4], weights=[70, 30])[0]
            
            self.grid[row][col] = spawn_value
    
    def can_move(self) -> bool:
        """Check if any moves are possible (DM: Graph connectivity analysis)"""
        # Check for empty cells
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return True
        
        # Check for adjacent equal tiles (DM: Graph adjacency)
        for r in range(self.size):
            for c in range(self.size):
                current = self.grid[r][c]
                # Check right neighbor
                if c < self.size - 1 and self.grid[r][c + 1] == current:
                    return True
                # Check down neighbor
                if r < self.size - 1 and self.grid[r + 1][c] == current:
                    return True
        
        return False
    
    def move(self, direction: str) -> bool:
        """Execute move with matrix transformations (DM: Linear algebra)"""
        old_grid = [row[:] for row in self.grid]
        old_score = self.score
        
        moved = False
        
        if direction == 'left':
            moved = self._move_left()
        elif direction == 'right':
            moved = self._move_right()
        elif direction == 'up':
            moved = self._move_up()
        elif direction == 'down':
            moved = self._move_down()
        
        if moved:
            # Save state for undo (DM: Stack data structure)
            self.move_history.append({
                'grid': old_grid,
                'score': old_score
            })
            # Limit undo history to 5 moves
            if len(self.move_history) > 5:
                self.move_history.pop(0)
            
            self.spawn_new_tile()
            return True
        
        return False
    
    def _move_left(self) -> bool:
        """Move tiles left using matrix row operations"""
        moved = False
        for r in range(self.size):
            # Compress row (remove zeros)
            compressed = [val for val in self.grid[r] if val != 0]
            
            # Merge adjacent equal values
            merged = []
            i = 0
            while i < len(compressed):
                if i < len(compressed) - 1 and compressed[i] == compressed[i + 1]:
                    # Merge tiles
                    merged_value = compressed[i] * 2
                    merged.append(merged_value)
                    self.score += merged_value
                    i += 2
                else:
                    merged.append(compressed[i])
                    i += 1
            
            # Pad with zeros
            new_row = merged + [0] * (self.size - len(merged))
            
            if new_row != self.grid[r]:
                moved = True
                self.grid[r] = new_row
        
        return moved
    
    def _move_right(self) -> bool:
        """Move tiles right (reverse of left)"""
        # Reverse each row, move left, then reverse back
        for r in range(self.size):
            self.grid[r] = self.grid[r][::-1]
        
        moved = self._move_left()
        
        for r in range(self.size):
            self.grid[r] = self.grid[r][::-1]
        
        return moved
    
    def _move_up(self) -> bool:
        """Move tiles up using matrix column operations"""
        # Transpose matrix, move left, transpose back
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self._move_left()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved
    
    def _move_down(self) -> bool:
        """Move tiles down (transpose, reverse, move left, reverse, transpose)"""
        self.grid = [list(row) for row in zip(*self.grid)]
        for r in range(self.size):
            self.grid[r] = self.grid[r][::-1]
        
        moved = self._move_left()
        
        for r in range(self.size):
            self.grid[r] = self.grid[r][::-1]
        self.grid = [list(row) for row in zip(*self.grid)]
        
        return moved
    
    def undo(self) -> bool:
        """Undo last move using stack (DM: Stack data structure)"""
        if self.move_history:
            last_state = self.move_history.pop()
            self.grid = last_state['grid']
            self.score = last_state['score']
            return True
        return False
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get list of empty cell coordinates (DM: Set theory)"""
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
    
    def clone(self):
        """Create deep copy of board state"""
        new_board = Board(self.size, self.difficulty)
        new_board.grid = [row[:] for row in self.grid]
        new_board.score = self.score
        return new_board

# ========================================
# ARTIFICIAL INTELLIGENCE: HEURISTICS
# ========================================

def calculate_heuristics(board: Board, weights: Dict[str, float] = None) -> Dict[str, float]:
    """
    Calculate multiple heuristics for board evaluation (AI: Evaluation functions)
    
    Heuristics used:
    1. Empty tiles: More empty = better (encourages space)
    2. Smoothness: Adjacent tiles with similar values = better
    3. Monotonicity: Tiles increase/decrease in order = better
    4. Corner reward: High values in corners = better
    """
    if weights is None:
        weights = {'empty': 0.25, 'smoothness': 0.25, 'monotonicity': 0.25, 'corner': 0.25}
    
    grid = board.grid
    size = board.size
    
    # 1. Empty tiles heuristic
    empty_count = len(board.get_empty_cells())
    empty_score = empty_count * 10
    
    # 2. Smoothness heuristic
    smoothness = 0
    for r in range(size):
        for c in range(size):
            if grid[r][c] != 0:
                value = math.log2(grid[r][c])
                # Check right neighbor
                if c < size - 1 and grid[r][c + 1] != 0:
                    neighbor_value = math.log2(grid[r][c + 1])
                    smoothness -= abs(value - neighbor_value)
                # Check down neighbor
                if r < size - 1 and grid[r + 1][c] != 0:
                    neighbor_value = math.log2(grid[r + 1][c])
                    smoothness -= abs(value - neighbor_value)
    
    # 3. Monotonicity heuristic
    monotonicity = 0
    
    # Check rows
    for r in range(size):
        inc = dec = 0
        for c in range(size - 1):
            if grid[r][c] != 0 and grid[r][c + 1] != 0:
                if grid[r][c] <= grid[r][c + 1]:
                    inc += math.log2(grid[r][c + 1]) - math.log2(grid[r][c])
                else:
                    dec += math.log2(grid[r][c]) - math.log2(grid[r][c + 1])
        monotonicity += max(inc, dec)
    
    # Check columns
    for c in range(size):
        inc = dec = 0
        for r in range(size - 1):
            if grid[r][c] != 0 and grid[r + 1][c] != 0:
                if grid[r][c] <= grid[r + 1][c]:
                    inc += math.log2(grid[r + 1][c]) - math.log2(grid[r][c])
                else:
                    dec += math.log2(grid[r][c]) - math.log2(grid[r + 1][c])
        monotonicity += max(inc, dec)
    
    # 4. Corner reward heuristic
    corner_bonus = 0
    corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
    max_tile = max(max(row) for row in grid)
    
    for r, c in corners:
        if grid[r][c] == max_tile:
            corner_bonus = max_tile * 2
            break
    
    # Combine heuristics with weights
    heuristics = {
        'empty': empty_score,
        'smoothness': smoothness,
        'monotonicity': monotonicity,
        'corner': corner_bonus
    }
    
    # Calculate weighted total
    total_score = sum(heuristics[key] * weights[key] for key in weights)
    heuristics['total'] = total_score
    
    return heuristics

# ========================================
# AI AGENTS
# ========================================

def greedy_agent(board: Board, weights: Dict[str, float] = None) -> Optional[str]:
    """
    Greedy AI agent using heuristic evaluation (AI: Greedy algorithms)
    
    Evaluates each possible move and chooses the one with highest heuristic score.
    """
    if weights is None:
        weights = {'empty': 0.25, 'smoothness': 0.25, 'monotonicity': 0.25, 'corner': 0.25}
    
    best_move = None
    best_score = float('-inf')
    
    for direction in ['up', 'down', 'left', 'right']:
        # Simulate move
        test_board = board.clone()
        if test_board.move(direction):
            heuristics = calculate_heuristics(test_board, weights)
            score = heuristics['total']
            
            if score > best_score:
                best_score = score
                best_move = direction
    
    return best_move

def expectimax_agent(board: Board, depth: int = 3, weights: Dict[str, float] = None) -> Optional[str]:
    """
    Expectimax AI agent (AI: Game tree search with chance nodes)
    
    Uses minimax with expectation over random tile spawns.
    Depth-limited search with heuristic evaluation at leaves.
    """
    if weights is None:
        weights = {'empty': 0.25, 'smoothness': 0.25, 'monotonicity': 0.25, 'corner': 0.25}
    
    def expectimax_search(board: Board, depth: int, is_player_turn: bool) -> float:
        if depth == 0 or not board.can_move():
            return calculate_heuristics(board, weights)['total']
        
        if is_player_turn:
            # Maximize over player moves
            max_score = float('-inf')
            for direction in ['up', 'down', 'left', 'right']:
                test_board = board.clone()
                if test_board.move(direction):
                    score = expectimax_search(test_board, depth - 1, False)
                    max_score = max(max_score, score)
            return max_score if max_score != float('-inf') else 0
        else:
            # Expectation over random tile spawns
            empty_cells = board.get_empty_cells()
            if not empty_cells:
                return calculate_heuristics(board, weights)['total']
            
            expected_score = 0
            for r, c in empty_cells:
                # Try spawning 2 (90% probability)
                test_board = board.clone()
                test_board.grid[r][c] = 2
                score_2 = expectimax_search(test_board, depth - 1, True)
                
                # Try spawning 4 (10% probability)
                test_board.grid[r][c] = 4
                score_4 = expectimax_search(test_board, depth - 1, True)
                
                expected_score += (0.9 * score_2 + 0.1 * score_4) / len(empty_cells)
            
            return expected_score
    
    best_move = None
    best_score = float('-inf')
    
    for direction in ['up', 'down', 'left', 'right']:
        test_board = board.clone()
        if test_board.move(direction):
            score = expectimax_search(test_board, depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = direction
    
    return best_move

# ========================================
# VISUAL EFFECTS & ANIMATIONS
# ========================================

class EaseType(Enum):
    LINEAR = "linear"
    EASE_OUT_CUBIC = "ease_out_cubic"
    EASE_IN_OUT_CUBIC = "ease_in_out_cubic"
    BOUNCE = "bounce"

class AnimationType(Enum):
    MOVE = "move"
    MERGE = "merge"
    SPAWN = "spawn"

@dataclass
class TileAnimation:
    tile_id: int
    animation_type: AnimationType
    start_time: float
    duration: float
    start_value: tuple
    end_value: tuple
    ease_type: EaseType = EaseType.EASE_OUT_CUBIC

class AnimationSystem:
    """Frame-rate independent animation system"""
    
    def __init__(self):
        self.active_animations: Dict[int, TileAnimation] = {}
        self.animation_speed = 1.0
    
    def ease_out_cubic(self, t: float) -> float:
        return 1 - pow(1 - t, 3)
    
    def ease_in_out_cubic(self, t: float) -> float:
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2
    
    def bounce_ease(self, t: float) -> float:
        if t < 0.36:
            return 7.5625 * t * t
        elif t < 0.72:
            return 7.5625 * (t - 0.54) * (t - 0.54) + 0.75
        elif t < 0.9:
            return 7.5625 * (t - 0.81) * (t - 0.81) + 0.9375
        else:
            return 7.5625 * (t - 0.955) * (t - 0.955) + 0.984375
    
    def get_easing_function(self, ease_type: EaseType) -> Callable:
        easing_map = {
            EaseType.LINEAR: lambda t: t,
            EaseType.EASE_OUT_CUBIC: self.ease_out_cubic,
            EaseType.EASE_IN_OUT_CUBIC: self.ease_in_out_cubic,
            EaseType.BOUNCE: self.bounce_ease
        }
        return easing_map.get(ease_type, self.ease_out_cubic)
    
    def animate_merge(self, tile_id: int, duration: float = 0.15):
        animation = TileAnimation(
            tile_id=tile_id,
            animation_type=AnimationType.MERGE,
            start_time=time.time(),
            duration=duration / self.animation_speed,
            start_value=(1.0,),
            end_value=(1.15,),
            ease_type=EaseType.BOUNCE
        )
        self.active_animations[tile_id] = animation
    
    def animate_spawn(self, tile_id: int, duration: float = 0.2):
        animation = TileAnimation(
            tile_id=tile_id,
            animation_type=AnimationType.SPAWN,
            start_time=time.time(),
            duration=duration / self.animation_speed,
            start_value=(0.6, 0.0),
            end_value=(1.0, 1.0),
            ease_type=EaseType.EASE_OUT_CUBIC
        )
        self.active_animations[tile_id] = animation
    
    def update(self, current_time: float) -> Dict[int, dict]:
        animation_states = {}
        completed = []
        
        for tile_id, animation in self.active_animations.items():
            elapsed = current_time - animation.start_time
            progress = min(1.0, elapsed / animation.duration)
            
            if progress >= 1.0:
                completed.append(tile_id)
                continue
            
            easing_func = self.get_easing_function(animation.ease_type)
            eased_progress = easing_func(progress)
            
            if animation.animation_type == AnimationType.MERGE:
                start_scale = animation.start_value[0]
                end_scale = animation.end_value[0]
                current_scale = start_scale + (end_scale - start_scale) * eased_progress
                animation_states[tile_id] = {'type': 'merge', 'scale': current_scale}
            elif animation.animation_type == AnimationType.SPAWN:
                start_scale, start_alpha = animation.start_value
                end_scale, end_alpha = animation.end_value
                current_scale = start_scale + (end_scale - start_scale) * eased_progress
                current_alpha = start_alpha + (end_alpha - start_alpha) * eased_progress
                animation_states[tile_id] = {'type': 'spawn', 'scale': current_scale, 'alpha': current_alpha}
        
        for tile_id in completed:
            del self.active_animations[tile_id]
        
        return animation_states
    
    def is_animating(self) -> bool:
        return len(self.active_animations) > 0

class ParticleSystem:
    """Particle effects for visual feedback"""
    
    def __init__(self):
        self.particles = []
    
    def create_burst(self, position: tuple, color: tuple, count: int = 12):
        center_x, center_y = position
        
        for i in range(count):
            angle = (2 * math.pi * i) / count
            speed = random.uniform(50, 150)
            
            particle = {
                'x': center_x,
                'y': center_y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'decay': random.uniform(0.02, 0.04),
                'size': random.randint(3, 8),
                'color': color
            }
            self.particles.append(particle)
    
    def update(self, dt: float):
        active_particles = []
        
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += 200 * dt  # Gravity
            particle['vx'] *= 0.98  # Friction
            particle['vy'] *= 0.98
            particle['life'] -= particle['decay']
            
            if particle['life'] > 0:
                active_particles.append(particle)
        
        self.particles = active_particles
    
    def draw(self, screen: pygame.Surface):
        for particle in self.particles:
            alpha = int(255 * particle['life'])
            size = int(particle['size'] * particle['life'])
            
            if size > 0:
                pos = (int(particle['x']), int(particle['y']))
                color = (*particle['color'], alpha)
                
                # Draw particle with glow
                particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (size, size), size)
                screen.blit(particle_surface, (pos[0] - size, pos[1] - size))

# ========================================
# FUTURISTIC UI COMPONENTS
# ========================================

class BackgroundRenderer:
    """Animated gradient background with particles"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.particles = []
        self.time = 0
        
        for _ in range(40):
            self.particles.append({
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.3, 0.3),
                'size': random.randint(1, 2),
                'alpha': random.randint(20, 60)
            })
    
    def update(self, dt: float):
        self.time += dt
        
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt * 60
            particle['y'] += particle['vy'] * dt * 60
            
            if particle['x'] < 0 or particle['x'] > self.width:
                particle['vx'] *= -1
            if particle['y'] < 0 or particle['y'] > self.height:
                particle['vy'] *= -1
    
    def draw(self, screen: pygame.Surface):
        # Gradient background
        for y in range(self.height):
            ratio = y / self.height
            r = int(COLORS['background_start'][0] * (1 - ratio) + COLORS['background_end'][0] * ratio)
            g = int(COLORS['background_start'][1] * (1 - ratio) + COLORS['background_end'][1] * ratio)
            b = int(COLORS['background_start'][2] * (1 - ratio) + COLORS['background_end'][2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (self.width, y))
        
        # Animated particles
        for particle in self.particles:
            pulse = math.sin(self.time * 2 + particle['x'] * 0.01) * 0.3 + 0.7
            alpha = int(particle['alpha'] * pulse)
            pos = (int(particle['x']), int(particle['y']))
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            color = (*COLORS['neon_cyan'], alpha)
            pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, (pos[0] - particle['size'], pos[1] - particle['size']))

class TileRenderer:
    """Advanced tile renderer with glassmorphic effects"""
    
    def draw_tile(self, screen: pygame.Surface, rect: pygame.Rect, value: int, scale: float = 1.0, alpha: float = 1.0):
        if scale != 1.0:
            center = rect.center
            new_size = int(rect.width * scale), int(rect.height * scale)
            rect = pygame.Rect(0, 0, new_size[0], new_size[1])
            rect.center = center
        
        color = TILE_COLORS.get(value, (100, 100, 100))
        
        # Create tile surface
        tile_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        tile_rect = pygame.Rect(10, 10, rect.width, rect.height)
        
        if value == 0:
            # Empty tile
            inset_color = (30, 40, 50, int(100 * alpha))
            self._draw_rounded_rect(tile_surface, inset_color, tile_rect, 16)
        else:
            # Filled tile with glow for high values
            if value >= 1024:
                self._draw_glow(tile_surface, tile_rect, color, alpha)
            
            # Main tile
            tile_color = (*color, int(255 * alpha))
            self._draw_rounded_rect(tile_surface, tile_color, tile_rect, 16)
            
            # Glassmorphic highlight
            highlight_rect = pygame.Rect(tile_rect.x + 2, tile_rect.y + 2,
                                       tile_rect.width - 4, tile_rect.height // 3)
            highlight_color = (*color, int(40 * alpha))
            self._draw_rounded_rect(tile_surface, highlight_color, highlight_rect, 12)
        
        # Blit to screen
        screen.blit(tile_surface, (rect.x - 10, rect.y - 10))
        
        # Draw text
        if value > 0:
            self._draw_text(screen, rect, value, alpha)
    
    def _draw_rounded_rect(self, surface: pygame.Surface, color: tuple, rect: pygame.Rect, radius: int):
        if len(color) == 4:  # RGBA
            temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, color, (0, 0, rect.width, rect.height), border_radius=radius)
            surface.blit(temp_surface, rect.topleft, special_flags=pygame.BLEND_ALPHA_SDL2)
        else:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def _draw_glow(self, surface: pygame.Surface, rect: pygame.Rect, color: tuple, alpha: float):
        for i in range(3):
            glow_rect = pygame.Rect(rect.x - i * 5, rect.y - i * 5,
                                  rect.width + i * 10, rect.height + i * 10)
            glow_color = (*color, int(20 * alpha))
            self._draw_rounded_rect(surface, glow_color, glow_rect, 20)
    
    def _draw_text(self, surface: pygame.Surface, rect: pygame.Rect, value: int, alpha: float):
        font_size = 36 if value >= 1024 else 42 if value >= 128 else 46  # Increased all sizes
        font = pygame.font.Font(None, font_size)
        
        # Better text color logic for visibility on all backgrounds
        # Dark text for light tiles (2, 4, 16, 512, 1024), white text for dark tiles
        if value in [2, 4, 16, 512, 1024]:
            text_color = (0, 0, 0, int(255 * alpha))  # Black text for bright backgrounds
        else:
            text_color = (255, 255, 255, int(255 * alpha))  # White text for dark backgrounds
        
        text = str(value)
        
        # Create text surface with alpha
        text_surface = font.render(text, True, text_color[:3])
        if alpha < 1.0:
            alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, int(255 * alpha)))
            text_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

class ControlPanel:
    """Glassmorphic control panel with sliders and displays"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 28)  # Increased from 24
        self.small_font = pygame.font.Font(None, 24)  # Increased from 20
        self.large_font = pygame.font.Font(None, 32)  # Increased from 28
        self.title_font = pygame.font.Font(None, 36)  # Increased from 32
        
        # State
        self.ai_enabled = False
        self.current_agent = "Human"
        self.expectimax_depth = 3
        self.animation_speed = 1.0
        self.heuristic_weights = {
            'empty': 0.25,
            'smoothness': 0.25,
            'monotonicity': 0.25,
            'corner': 0.25
        }
        
        # Tips section state
        self.show_tips = False
        self.tip_scroll_offset = 0
        self.tips_button_rect = pygame.Rect(0, 0, 200, 30)  # Will be updated in draw method
        
        # Feature buttons state (auto-solve and heatmap removed per user request)
        self.speed_mode = "Normal"  # Normal, Fast, Instant
        self.speed_button_rect = pygame.Rect(0, 0, 200, 30)
        self.difficulty = "Medium"  # Easy, Medium, Hard
        self.difficulty_button_rect = pygame.Rect(0, 0, 200, 30)
        
        # AI Tips content
        self.ai_tips = [
            "🎯 WINNING STRATEGIES",
            "",
            "• Keep highest tile in corner",
            "  The corner strategy is most effective",
            "",
            "• Build monotonic sequences", 
            "  Arrange tiles in descending order",
            "",
            "• Maintain empty spaces",
            "  More empty = more options",
            "",
            "• Avoid random movements",
            "  Think 2-3 moves ahead",
            "",
            "• Focus on one direction",
            "  Pick left/right as primary",
            "",
            "• Don't chase high merges",
            "  Build foundation first",
            "",
            "🤖 AI INSIGHTS",
            "",
            "• Greedy: Fast but short-sighted",
            "  Good for quick decisions",
            "",
            "• Expectimax: Strategic planner", 
            "  Considers future possibilities",
            "",
            "• Depth 3-4: Balanced performance",
            "  Higher = slower but smarter",
            "",
            "🏆 PRO TIPS",
            "",
            "• Use undo strategically",
            "  Learn from mistakes",
            "",
            "• Watch AI patterns",
            "  Learn optimal moves",
            "",
            "• Practice corner control",
            "  Master the fundamentals",
            "",
            "📋 NUMBERED STRATEGIES",
            "",
            "1. Corner Lock Strategy",
            "   Keep highest tile in one corner",
            "   and build around it systematically",
            "",
            "2. Snake Pattern Method", 
            "   Arrange tiles in descending",
            "   zigzag pattern for stability",
            "",
            "3. Edge Building Technique",
            "   Build highest values along",
            "   one edge, then fill inward",
            "",
            "4. Two-Direction Rule",
            "   Use only left/right OR up/down",
            "   to maintain tile organization",
            "",
            "5. Empty Cell Management",
            "   Always keep 25% of board empty",
            "   for maximum move flexibility",
            "",
            "🎮 ADVANCED TACTICS",
            "",
            "• Pattern Recognition",
            "  Study successful AI moves",
            "",
            "• Risk Assessment", 
            "  Evaluate each move's safety",
            "",
            "• Tile Value Planning",
            "  Think 3-5 moves ahead"
        ]
    
    def draw(self, screen: pygame.Surface, game_stats: dict, heuristics: dict = None):
        # Panel background
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        bg_color = COLORS['panel_bg']
        pygame.draw.rect(panel_surface, bg_color, (0, 0, self.rect.width, self.rect.height), border_radius=15)
        
        # Border
        border_color = COLORS['panel_border']
        pygame.draw.rect(panel_surface, border_color, (0, 0, self.rect.width, self.rect.height), 2, border_radius=15)
        
        screen.blit(panel_surface, self.rect.topleft)
        
        # Title with better styling
        title = self.title_font.render("CONTROL PANEL", True, COLORS['neon_cyan'])
        title_rect = title.get_rect(centerx=self.rect.centerx, y=self.rect.y + 15)
        screen.blit(title, title_rect)
        
        # Add decorative line under title
        line_start = (self.rect.x + 30, self.rect.y + 50)
        line_end = (self.rect.right - 30, self.rect.y + 50)
        pygame.draw.line(screen, COLORS['neon_cyan'], line_start, line_end, 2)
        
        y_offset = 70
        
        # Game stats with better formatting
        stats_title = self.title_font.render("📊 GAME STATUS", True, COLORS['electric_orange'])
        screen.blit(stats_title, (self.rect.x + 20, self.rect.y + y_offset))
        y_offset += 40
        
        # Make current score more prominent
        current_score = f"Score: {game_stats.get('score', 0):,}"
        score_text = self.large_font.render(current_score, True, COLORS['neon_cyan'])
        screen.blit(score_text, (self.rect.x + 30, self.rect.y + y_offset))
        y_offset += 35
        
        # Other stats with regular styling
        other_stats = [
            f"Best: {game_stats.get('best_score', 0):,}",
            f"Moves: {game_stats.get('moves', 0)}",
            f"Mode: {self.current_agent}",
        ]
        
        for stat in other_stats:
            text = self.font.render(stat, True, (255, 255, 255))  # Use larger font
            screen.blit(text, (self.rect.x + 30, self.rect.y + y_offset))
            y_offset += 30  # Increased spacing
        
        # Game balance indicator
        balance_text = "✨ Adaptive Spawning: ON"
        balance_display = self.small_font.render(balance_text, True, COLORS['lime_green'])
        screen.blit(balance_display, (self.rect.x + 30, self.rect.y + y_offset))
        y_offset += 25
        
        # AI Controls section
        y_offset += 25  # Increased spacing
        ai_title = self.title_font.render("🤖 AI CONTROLS", True, COLORS['deep_pink'])
        screen.blit(ai_title, (self.rect.x + 20, self.rect.y + y_offset))
        y_offset += 40  # Increased spacing
        
        # AI Status with better visual feedback
        ai_status = "ACTIVE" if self.ai_enabled else "MANUAL"
        ai_color = COLORS['lime_green'] if self.ai_enabled else (150, 150, 150)
        ai_display = self.font.render(f"Status: {ai_status}", True, ai_color)  # Use larger font
        screen.blit(ai_display, (self.rect.x + 30, self.rect.y + y_offset))
        y_offset += 30  # Increased spacing
        
        # Agent selection
        agent_display = self.font.render(f"Agent: {self.current_agent}", True, (255, 255, 255))  # Use larger font
        screen.blit(agent_display, (self.rect.x + 30, self.rect.y + y_offset))
        y_offset += 30  # Increased spacing
        
        # Expectimax depth
        depth_text = self.font.render(f"Depth: {self.expectimax_depth}", True, (200, 200, 200))  # Use larger font
        screen.blit(depth_text, (self.rect.x + 30, self.rect.y + y_offset))
        y_offset += 40  # Increased spacing
        
        # Heuristics display
        if heuristics and self.current_agent != "Human":
            heur_title = self.font.render("📈 HEURISTICS", True, COLORS['gold'])
            screen.blit(heur_title, (self.rect.x + 20, self.rect.y + y_offset))
            y_offset += 35
            
            for key, value in heuristics.items():
                if key != 'total':
                    heur_text = f"{key.title()}: {value:.1f}"
                    text = self.small_font.render(heur_text, True, (200, 200, 200))
                    screen.blit(text, (self.rect.x + 30, self.rect.y + y_offset))
                    y_offset += 22
            
            # Total score
            total_text = f"Total: {heuristics.get('total', 0):.1f}"
            total_display = self.small_font.render(total_text, True, COLORS['neon_cyan'])
            screen.blit(total_display, (self.rect.x + 30, self.rect.y + y_offset))
            y_offset += 35
        
        # Game Settings Section
        y_offset += 15
        features_title = self.title_font.render("⚙️ GAME SETTINGS", True, COLORS['neon_magenta'])
        screen.blit(features_title, (self.rect.x + 20, self.rect.y + y_offset))
        y_offset += 45
        
        # Speed Mode Button (larger and more prominent)
        self.speed_button_rect = pygame.Rect(self.rect.x + 20, self.rect.y + y_offset, 220, 40)
        speed_colors = {"Normal": (60, 80, 100), "Fast": COLORS['electric_orange'], "Instant": COLORS['red_orange']}
        speed_color = speed_colors.get(self.speed_mode, (60, 80, 100))
        speed_surface = pygame.Surface((220, 40), pygame.SRCALPHA)
        pygame.draw.rect(speed_surface, (*speed_color[:3], 180), (0, 0, 220, 40), border_radius=10)
        pygame.draw.rect(speed_surface, COLORS['neon_cyan'], (0, 0, 220, 40), 3, border_radius=10)
        screen.blit(speed_surface, self.speed_button_rect.topleft)
        
        speed_text = f"🏃 Speed: {self.speed_mode}"
        speed_label = self.font.render(speed_text, True, (255, 255, 255))
        speed_label_rect = speed_label.get_rect(center=self.speed_button_rect.center)
        screen.blit(speed_label, speed_label_rect)
        y_offset += 50
        
        # Difficulty Button (larger and more prominent)
        self.difficulty_button_rect = pygame.Rect(self.rect.x + 20, self.rect.y + y_offset, 220, 40)
        difficulty_colors = {"Easy": COLORS['lime_green'], "Medium": COLORS['electric_orange'], "Hard": COLORS['red_orange']}
        difficulty_color = difficulty_colors.get(self.difficulty, (60, 80, 100))
        difficulty_surface = pygame.Surface((220, 40), pygame.SRCALPHA)
        pygame.draw.rect(difficulty_surface, (*difficulty_color[:3], 180), (0, 0, 220, 40), border_radius=10)
        pygame.draw.rect(difficulty_surface, COLORS['neon_cyan'], (0, 0, 220, 40), 3, border_radius=10)
        screen.blit(difficulty_surface, self.difficulty_button_rect.topleft)
        
        difficulty_text = f"⚙️ {self.difficulty} Mode"
        difficulty_label = self.font.render(difficulty_text, True, (255, 255, 255))
        difficulty_label_rect = difficulty_label.get_rect(center=self.difficulty_button_rect.center)
        screen.blit(difficulty_label, difficulty_label_rect)
        y_offset += 55
        
        # Tips toggle button (larger and more prominent)
        self.tips_button_rect = pygame.Rect(self.rect.x + 20, self.rect.y + y_offset, 220, 40)
        button_color = COLORS['blue_violet'] if self.show_tips else (60, 80, 100)
        button_surface = pygame.Surface((220, 40), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*button_color[:3], 180), (0, 0, 220, 40), border_radius=10)
        pygame.draw.rect(button_surface, COLORS['gold'], (0, 0, 220, 40), 3, border_radius=10)
        screen.blit(button_surface, self.tips_button_rect.topleft)
        
        tips_text = self.font.render("💡 AI TIPS", True, (255, 255, 255))
        tips_text_rect = tips_text.get_rect(center=self.tips_button_rect.center)
        screen.blit(tips_text, tips_text_rect)
        y_offset += 55
        
        # Draw tips section if enabled
        if self.show_tips:
            self.draw_tips_section(screen, y_offset)
        else:
            # Controls help when tips not shown
            help_title = self.font.render("⌨️ CONTROLS", True, COLORS['electric_orange'])
            screen.blit(help_title, (self.rect.x + 20, self.rect.y + y_offset))
            y_offset += 35
            
            controls = [
                "Arrow Keys: Move tiles",
                "A: Toggle AI mode", 
                "M: Switch agent",
                "R: Reset game",
                "U: Undo move (5 max)",
                "↑↓: Adjust AI depth",
                "Click tips for strategies"
            ]
            
            for control in controls:
                text = self.small_font.render(control, True, (180, 180, 180))
                screen.blit(text, (self.rect.x + 30, self.rect.y + y_offset))
                y_offset += 22
    
    def draw_tips_section(self, screen: pygame.Surface, start_y: int):
        """Draw the AI tips and strategies section"""
        tips_area = pygame.Rect(self.rect.x + 10, self.rect.y + start_y, 
                               self.rect.width - 20, self.rect.height - start_y - 20)
        
        # Tips background
        tips_surface = pygame.Surface((tips_area.width, tips_area.height), pygame.SRCALPHA)
        tips_bg = (10, 20, 40, 180)
        pygame.draw.rect(tips_surface, tips_bg, (0, 0, tips_area.width, tips_area.height), border_radius=10)
        pygame.draw.rect(tips_surface, COLORS['neon_cyan'], (0, 0, tips_area.width, tips_area.height), 1, border_radius=10)
        screen.blit(tips_surface, tips_area.topleft)
        
        # Render tips with scrolling
        y_pos = 15
        max_lines = (tips_area.height - 30) // 22
        start_line = max(0, self.tip_scroll_offset)
        end_line = min(len(self.ai_tips), start_line + max_lines)
        
        for i in range(start_line, end_line):
            tip_line = self.ai_tips[i]
            if not tip_line.strip():  # Empty line
                y_pos += 22
                continue
                
            # Different colors for different types of content
            if tip_line.startswith("🎯") or tip_line.startswith("🤖") or tip_line.startswith("🏆"):
                color = COLORS['gold']
                font = self.font
            elif tip_line.startswith("•"):
                color = (220, 220, 220)
                font = self.small_font
            else:
                color = (180, 180, 180)
                font = self.small_font
            
            text = font.render(tip_line, True, color)
            screen.blit(text, (tips_area.x + 15, tips_area.y + y_pos))
            y_pos += 22
        
        # Scroll indicators if needed
        if len(self.ai_tips) > max_lines:
            if self.tip_scroll_offset > 0:
                # Up arrow
                up_arrow = "▲"
                arrow_text = self.small_font.render(up_arrow, True, COLORS['neon_cyan'])
                screen.blit(arrow_text, (tips_area.right - 25, tips_area.y + 10))
            
            if end_line < len(self.ai_tips):
                # Down arrow
                down_arrow = "▼" 
                arrow_text = self.small_font.render(down_arrow, True, COLORS['neon_cyan'])
                screen.blit(arrow_text, (tips_area.right - 25, tips_area.bottom - 25))
    
    def handle_tips_click(self, pos: tuple) -> bool:
        """Handle clicks on tips section"""
        if self.tips_button_rect.collidepoint(pos):
            self.show_tips = not self.show_tips
            return True
        return False
    
    def handle_tips_scroll(self, direction: int):
        """Handle scrolling in tips section"""
        if self.show_tips:
            self.tip_scroll_offset = max(0, min(len(self.ai_tips) - 10, 
                                               self.tip_scroll_offset + direction))
    
    def handle_button_click(self, pos: tuple) -> str:
        """Handle clicks on feature buttons, returns action type"""
        if self.speed_button_rect.collidepoint(pos):
            # Cycle through speed modes
            speed_order = ["Normal", "Fast", "Instant"]
            current_idx = speed_order.index(self.speed_mode)
            self.speed_mode = speed_order[(current_idx + 1) % len(speed_order)]
            return "speed_change"
        elif self.difficulty_button_rect.collidepoint(pos):
            # Cycle through difficulty levels
            difficulty_order = ["Easy", "Medium", "Hard"]
            current_idx = difficulty_order.index(self.difficulty)
            self.difficulty = difficulty_order[(current_idx + 1) % len(difficulty_order)]
            return "difficulty_change"
        elif self.tips_button_rect.collidepoint(pos):
            self.show_tips = not self.show_tips
            return "tips_toggle"
        return "none"

# ========================================
# SAVE/LOAD SYSTEM
# ========================================

def load_best_score() -> int:
    """Load best score from JSON file"""
    try:
        with open("best_score.json", "r") as f:
            return json.load(f)["best_score"]
    except:
        return 0

def save_best_score(score: int):
    """Save best score to JSON file"""
    with open("best_score.json", "w") as f:
        json.dump({"best_score": score}, f)

# ========================================
# MAIN GAME CLASS
# ========================================

class FuturisticGame2048:
    """Main game class integrating all systems"""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🚀 Futuristic 2048 - AI & DM Integration")
        self.clock = pygame.time.Clock()
        
        # Game components
        self.board = Board(BOARD_SIZE)
        self.background = BackgroundRenderer(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.tile_renderer = TileRenderer()
        self.animation_system = AnimationSystem()
        self.particle_system = ParticleSystem()
        self.control_panel = ControlPanel(950, 50, 400, WINDOW_HEIGHT - 100)
        
        # Title animation
        self.title_time = 0
        self.title_font = pygame.font.Font(None, 72)  # Increased from 64
        self.subtitle_font = pygame.font.Font(None, 32)  # Increased from 28
        
        # Game state
        self.running = True
        self.last_move_time = 0
        self.ai_move_delay = 0.5  # Seconds between AI moves
        # Note: auto_solve and heatmap features removed per user request
        
        # Stats
        self.game_stats = {
            'score': 0,
            'best_score': load_best_score(),
            'moves': 0
        }
        
        # Victory state
        self.won_2048 = False
        self.victory_time = 0
        self.show_victory = False
        
        # AI state
        self.last_heuristics = {}
        
        # Sound effects (optional - create simple tones)
        self.setup_sounds()
        
        print("🚀 Futuristic 2048 Game Started!")
        print("🎮 Controls:")
        print("   Arrow Keys: Move tiles")
        print("   A: Toggle AI mode")
        print("   M: Switch AI agent")
        print("   R: Reset game")
        print("   U: Undo last move")
        print("   F: Cycle speed mode")
        print("   D: Cycle difficulty")
        print("   +/-: Adjust AI depth")
        print("   ESC: Quit game")
        print("   💡 Click buttons in control panel for more features!")
    
    def setup_sounds(self):
        """Create simple sound effects"""
        try:
            # Create simple sound effects using pygame
            self.sounds = {
                'move': None,  # Placeholder
                'merge': None,  # Placeholder
                'win': None  # Placeholder
            }
        except:
            self.sounds = {}
    
    def play_sound(self, name: str):
        """Play a sound effect if available (safe no-op if not).

        Some environments may not have pygame.mixer or sound assets initialized.
        This helper ensures calls like self.play_sound('move') won't crash the game.
        """
        try:
            if not hasattr(self, 'sounds') or not self.sounds:
                return
            snd = self.sounds.get(name)
            if snd is None:
                return
            # If it's a pygame Sound object, play it
            if hasattr(snd, 'play'):
                snd.play()
            # If it's a fallback callable, call it
            elif callable(snd):
                snd()
        except Exception:
            # Fail silently to avoid crashing the game
            return
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.handle_keypress(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle clicks on control panel buttons
                action = self.control_panel.handle_button_click(event.pos)
                if action == "speed_change":
                    self.apply_speed_mode()
                    print(f"🏃 Speed mode: {self.control_panel.speed_mode}")
                elif action == "difficulty_change":
                    # Apply new difficulty to board
                    self.board.difficulty = self.control_panel.difficulty
                    print(f"⚙️ Difficulty: {self.control_panel.difficulty} (takes effect on next spawn)")
                elif action == "tips_toggle":
                    # Tips toggle is already handled in handle_button_click
                    print(f"💡 Tips {'shown' if self.control_panel.show_tips else 'hidden'}")
            
            elif event.type == pygame.MOUSEWHEEL:
                # Handle scrolling in tips section
                self.control_panel.handle_tips_scroll(-event.y)
    
    def handle_keypress(self, key):
        """Handle keyboard input"""
        # Dismiss victory overlay with any key
        if self.show_victory and key != pygame.K_ESCAPE:
            self.show_victory = False
            return
        
        # ESC key to quit (handle first to avoid conflicts)
        if key == pygame.K_ESCAPE:
            self.running = False
            print("👋 Game closed by user")
            return
        
        # Movement keys (only if not in AI mode or animations running)
        if not self.control_panel.ai_enabled and not self.animation_system.is_animating():
            move_made = False
            old_grid = [row[:] for row in self.board.grid]
            
            if key == pygame.K_UP:
                move_made = self.board.move('up')
            elif key == pygame.K_DOWN:
                move_made = self.board.move('down')
            elif key == pygame.K_LEFT:
                move_made = self.board.move('left')
            elif key == pygame.K_RIGHT:
                move_made = self.board.move('right')
            else:
                # Not an arrow key, continue to other key handlers
                pass
            
            if move_made:
                self.game_stats['moves'] += 1
                self.trigger_animations(old_grid, self.board.grid)
                self.play_sound('move')
                return  # Exit early after handling movement
            elif key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                # Arrow key pressed but no move made (blocked or no change)
                return
        
        # Game controls
        if key == pygame.K_a:
            self.control_panel.ai_enabled = not self.control_panel.ai_enabled
            print(f"AI {'enabled' if self.control_panel.ai_enabled else 'disabled'}")
        
        elif key == pygame.K_m:
            agents = ["Human", "Greedy", "Expectimax"]
            current_idx = agents.index(self.control_panel.current_agent)
            next_idx = (current_idx + 1) % len(agents)
            self.control_panel.current_agent = agents[next_idx]
            print(f"Switched to {agents[next_idx]} agent")
        
        elif key == pygame.K_r:
            self.reset_game()
        
        elif key == pygame.K_u:
            if self.board.undo():
                self.game_stats['moves'] = max(0, self.game_stats['moves'] - 1)
                print("Move undone")
        
        # Expectimax depth adjustment (using + and - keys)
        elif key == pygame.K_EQUALS or key == pygame.K_PLUS or key == pygame.K_KP_PLUS:
            self.control_panel.expectimax_depth = min(6, self.control_panel.expectimax_depth + 1)
            print(f"Expectimax depth: {self.control_panel.expectimax_depth}")
        elif key == pygame.K_MINUS or key == pygame.K_KP_MINUS:
            self.control_panel.expectimax_depth = max(1, self.control_panel.expectimax_depth - 1)
            print(f"Expectimax depth: {self.control_panel.expectimax_depth}")
        
        # New feature shortcuts
        elif key == pygame.K_f:
            # Cycle speed mode
            speed_order = ["Normal", "Fast", "Instant"]
            current_idx = speed_order.index(self.control_panel.speed_mode)
            self.control_panel.speed_mode = speed_order[(current_idx + 1) % len(speed_order)]
            self.apply_speed_mode()
        elif key == pygame.K_d:
            # Cycle difficulty
            difficulty_order = ["Easy", "Medium", "Hard"]
            current_idx = difficulty_order.index(self.control_panel.difficulty)
            self.control_panel.difficulty = difficulty_order[(current_idx + 1) % len(difficulty_order)]
            self.board.difficulty = self.control_panel.difficulty
            print(f"⚙️ Difficulty: {self.control_panel.difficulty} (takes effect on next spawn)")
    
    def trigger_animations(self, old_grid, new_grid):
        """Trigger appropriate animations based on grid changes"""
        board_y_offset = 130  # Match the offset used in draw method
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                tile_id = r * BOARD_SIZE + c
                old_val = old_grid[r][c]
                new_val = new_grid[r][c]
                
                if old_val != new_val:
                    if new_val > old_val and old_val != 0:
                        # Merge occurred
                        self.animation_system.animate_merge(tile_id)
                        if new_val >= 128:
                            # Particle burst for big merges
                            pos = (50 + c * (CELL_SIZE + MARGIN) + CELL_SIZE // 2,
                                  50 + r * (CELL_SIZE + MARGIN) + CELL_SIZE // 2 + board_y_offset)
                            color = TILE_COLORS.get(new_val, COLORS['pure_white'])
                            self.particle_system.create_burst(pos, color)
                            self.play_sound('merge')
                    
                    elif old_val == 0 and new_val > 0:
                        # New tile spawned
                        self.animation_system.animate_spawn(tile_id)
    
    def update_ai(self):
        """Update AI decision making"""
        if not self.control_panel.ai_enabled or self.animation_system.is_animating():
            return
        
        current_time = time.time()
        if current_time - self.last_move_time < self.ai_move_delay:
            return
        
        agent = self.control_panel.current_agent
        move = None
        
        start_time = time.time()
        
        try:
            if agent == "Greedy":
                move = greedy_agent(self.board, self.control_panel.heuristic_weights)
            elif agent == "Expectimax":
                move = expectimax_agent(self.board, self.control_panel.expectimax_depth, 
                                      self.control_panel.heuristic_weights)
        except Exception as e:
            print(f"AI Error: {e}")
        
        decision_time = time.time() - start_time
        print(f"AI ({agent}) decision time: {decision_time:.3f}s")
        
        if move:
            old_grid = [row[:] for row in self.board.grid]
            if self.board.move(move):
                self.game_stats['moves'] += 1
                self.trigger_animations(old_grid, self.board.grid)
                self.last_move_time = current_time
                self.play_sound('move')
        else:
            # No valid moves available
            self.control_panel.ai_enabled = False
            print("No valid moves - AI disabled")
    
    def reset_game(self):
        """Reset the game to initial state"""
        if self.board.score > self.game_stats['best_score']:
            self.game_stats['best_score'] = self.board.score
            save_best_score(self.board.score)
        
        self.board = Board(BOARD_SIZE, self.control_panel.difficulty)
        self.animation_system = AnimationSystem()
        self.particle_system = ParticleSystem()
        self.game_stats['moves'] = 0
        self.won_2048 = False
        self.show_victory = False
        print(f"🎮 Game reset! Difficulty: {self.control_panel.difficulty}")
    
    def apply_speed_mode(self):
        """Apply the selected speed mode"""
        speed_settings = {
            "Normal": (0.3, 1.0),   # (ai_delay, animation_speed)
            "Fast": (0.05, 3.0),    # Faster AI, quicker animations
            "Instant": (0.0, 10.0)  # No delay, instant animations
        }
        
        if self.control_panel.speed_mode in speed_settings:
            delay, anim_speed = speed_settings[self.control_panel.speed_mode]
            self.ai_move_delay = delay
            self.animation_system.animation_speed = anim_speed
    
    def update(self):
        """Update all game systems"""
        current_time = time.time()
        dt = self.clock.get_time() / 1000.0
        
        # Update title animation
        self.title_time += dt
        
        # Update visual systems
        self.background.update(dt)
        self.particle_system.update(dt)
        
        # Update AI
        self.update_ai()
        
        # Update game stats
        self.game_stats['score'] = self.board.score
        
        # Check for 2048 victory
        if not self.won_2048:
            max_tile = max(max(row) for row in self.board.grid)
            if max_tile >= 2048:
                self.won_2048 = True
                self.show_victory = True
                self.victory_time = current_time
                print("🏆🎉 CONGRATULATIONS! You reached 2048! 🎉🏆")
        
        # Calculate heuristics for display
        if self.control_panel.current_agent != "Human":
            self.last_heuristics = calculate_heuristics(self.board, self.control_panel.heuristic_weights)
    
    def draw_animated_title(self):
        """Draw animated game title at the top"""
        # Main title with glow effect
        pulse = math.sin(self.title_time * 2) * 0.3 + 0.7
        
        # Title text
        title_text = "FUTURISTIC 2048"
        title_surface = self.title_font.render(title_text, True, COLORS['pure_white'])
        
        # Create glow effect
        glow_surface = self.title_font.render(title_text, True, COLORS['neon_cyan'])
        
        # Position at top center
        title_rect = title_surface.get_rect(centerx=WINDOW_WIDTH // 2, y=10)
        glow_rect = glow_surface.get_rect(centerx=WINDOW_WIDTH // 2, y=10)
        
        # Draw multiple glow layers for better effect
        for offset in range(1, 4):
            glow_alpha = int(30 * pulse / offset)
            temp_surface = pygame.Surface(glow_surface.get_size(), pygame.SRCALPHA)
            temp_surface.fill((*COLORS['neon_cyan'], glow_alpha))
            glow_copy = glow_surface.copy()
            glow_copy.blit(temp_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
            
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    if dx != 0 or dy != 0:
                        self.screen.blit(glow_copy, (glow_rect.x + dx, glow_rect.y + dy))
        
        # Draw main title
        self.screen.blit(title_surface, title_rect)
        
        # Animated decorative line under title
        line_y = 75
        line_length = int(250 + 40 * math.sin(self.title_time * 3))
        line_start = WINDOW_WIDTH // 2 - line_length // 2
        line_end = WINDOW_WIDTH // 2 + line_length // 2
        
        # Draw gradient line
        for i in range(0, line_length, 2):
            progress = i / line_length
            r = int(COLORS['neon_cyan'][0] * (1 - progress) + COLORS['neon_magenta'][0] * progress)
            g = int(COLORS['neon_cyan'][1] * (1 - progress) + COLORS['neon_magenta'][1] * progress)  
            b = int(COLORS['neon_cyan'][2] * (1 - progress) + COLORS['neon_magenta'][2] * progress)
            
            pygame.draw.line(self.screen, (r, g, b), 
                           (line_start + i, line_y), (line_start + i + 1, line_y), 3)
    
    def draw(self):
        """Render the complete game"""
        # Background
        self.background.draw(self.screen)
        
        # Animated title at top
        self.draw_animated_title()
        
        # Game board background (positioned optimally after removing subtitle)
        board_y_offset = 100  # Reduced from 130 to better utilize space
        board_bg = pygame.Surface((CELL_SIZE * 4 + MARGIN * 5, CELL_SIZE * 4 + MARGIN * 5), pygame.SRCALPHA)
        bg_color = (30, 40, 60, 180)  # Increased opacity for better visibility
        pygame.draw.rect(board_bg, bg_color, (0, 0, board_bg.get_width(), board_bg.get_height()), border_radius=20)
        self.screen.blit(board_bg, (30, 30 + board_y_offset))
        
        # Get animation states
        animation_states = self.animation_system.update(time.time())
        
        # Draw tiles (adjusted position)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                tile_id = r * BOARD_SIZE + c
                value = self.board.grid[r][c]
                
                x = 50 + c * (CELL_SIZE + MARGIN)
                y = 50 + r * (CELL_SIZE + MARGIN) + board_y_offset
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # Apply animations
                scale = 1.0
                alpha = 1.0
                
                if tile_id in animation_states:
                    state = animation_states[tile_id]
                    if state['type'] == 'merge':
                        scale = state['scale']
                    elif state['type'] == 'spawn':
                        scale = state['scale']
                        alpha = state['alpha']
                
                self.tile_renderer.draw_tile(self.screen, rect, value, scale, alpha)
        
        # Draw particles
        self.particle_system.draw(self.screen)
        
        # Draw control panel
        self.control_panel.draw(self.screen, self.game_stats, self.last_heuristics)
        
        # Draw bottom instructions for better UI guidance
        instruction_font = pygame.font.Font(None, 24)  # Slightly larger for better readability
        instructions = [
            "🎮 Arrows: Move  •  A: Toggle AI  •  M: Switch Agent  •  R: Reset  •  U: Undo",
            "🔧 F: Speed Mode  •  D: Difficulty  •  +/-: AI Depth  •  Click Panel Buttons  •  ESC: Quit"
        ]
        
        y_pos = WINDOW_HEIGHT - 60
        for instruction in instructions:
            text = instruction_font.render(instruction, True, (180, 200, 220))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
            
            # Add subtle background for readability
            bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((10, 20, 30, 120))
            self.screen.blit(bg_surface, bg_rect.topleft)
            
            self.screen.blit(text, text_rect)
            y_pos += 25
        
        # Game over overlay
        if not self.board.can_move() and not self.animation_system.is_animating():
            self.draw_game_over()
        
        # Victory overlay
        if self.show_victory:
            self.draw_victory_overlay()
        
        pygame.display.flip()
    
    def draw_victory_overlay(self):
        """Draw victory overlay when 2048 is achieved"""
        # Semi-transparent overlay with golden tint
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 215, 0, 120))  # Golden overlay
        self.screen.blit(overlay, (0, 0))
        
        # Animated pulse effect
        pulse = math.sin(time.time() * 3) * 0.2 + 0.8
        
        # Victory panel
        panel_width = 700
        panel_height = 400
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2
        
        # Panel background with glow
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (20, 30, 50, 240), (0, 0, panel_width, panel_height), border_radius=30)
        
        # Glowing border
        for i in range(3):
            border_rect = pygame.Rect(-i*3, -i*3, panel_width + i*6, panel_height + i*6)
            alpha = int(80 * pulse / (i + 1))
            pygame.draw.rect(panel_surface, (*COLORS['gold'], alpha), border_rect, 5, border_radius=30)
        
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        # Main victory text with glow
        victory_font = pygame.font.Font(None, 96)
        victory_text = "🎉 CONGRATULATIONS! 🎉"
        
        # Draw glow layers
        for offset in range(1, 4):
            glow_alpha = int(60 * pulse / offset)
            glow_surface = victory_font.render(victory_text, True, COLORS['gold'])
            glow_temp = pygame.Surface(glow_surface.get_size(), pygame.SRCALPHA)
            glow_temp.fill((*COLORS['gold'], glow_alpha))
            glow_surface.blit(glow_temp, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
            
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    if dx != 0 or dy != 0:
                        text_rect = glow_surface.get_rect(center=(WINDOW_WIDTH//2 + dx, panel_y + 80 + dy))
                        self.screen.blit(glow_surface, text_rect)
        
        # Main text
        main_text = victory_font.render(victory_text, True, COLORS['pure_white'])
        main_rect = main_text.get_rect(center=(WINDOW_WIDTH//2, panel_y + 80))
        self.screen.blit(main_text, main_rect)
        
        # Achievement text
        achievement_font = pygame.font.Font(None, 64)
        achievement = achievement_font.render("You reached 2048!", True, COLORS['gold'])
        achievement_rect = achievement.get_rect(center=(WINDOW_WIDTH//2, panel_y + 160))
        self.screen.blit(achievement, achievement_rect)
        
        # Separator line
        line_y = panel_y + 210
        line_length = 500
        line_start = (WINDOW_WIDTH//2 - line_length//2, line_y)
        line_end = (WINDOW_WIDTH//2 + line_length//2, line_y)
        pygame.draw.line(self.screen, COLORS['gold'], line_start, line_end, 3)
        
        # Score display
        score_font = pygame.font.Font(None, 48)
        score_text = f"Score: {self.board.score:,}"
        score_surface = score_font.render(score_text, True, COLORS['neon_cyan'])
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH//2, panel_y + 260))
        self.screen.blit(score_surface, score_rect)
        
        # Moves display
        moves_text = f"Moves: {self.game_stats['moves']}"
        moves_surface = score_font.render(moves_text, True, COLORS['lime_green'])
        moves_rect = moves_surface.get_rect(center=(WINDOW_WIDTH//2, panel_y + 310))
        self.screen.blit(moves_surface, moves_rect)
        
        # Continue instruction with pulsing effect
        instruction_font = pygame.font.Font(None, 36)
        instruction_alpha = int(255 * pulse)
        instruction = "Press any key to continue playing..."
        instruction_surface = instruction_font.render(instruction, True, COLORS['pure_white'])
        instruction_temp = pygame.Surface(instruction_surface.get_size(), pygame.SRCALPHA)
        instruction_temp.fill((255, 255, 255, instruction_alpha))
        instruction_surface.blit(instruction_temp, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH//2, panel_y + 360))
        self.screen.blit(instruction_surface, instruction_rect)
    
    def draw_game_over(self):
        """Draw game over overlay"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 84)  # Increased from 72
        game_over_text = font.render("GAME OVER", True, COLORS['red_orange'])
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        score_font = pygame.font.Font(None, 56)  # Increased from 48
        final_score = score_font.render(f"Final Score: {self.board.score}", True, COLORS['pure_white'])
        score_rect = final_score.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
        self.screen.blit(final_score, score_rect)
        
        # Check for new best score
        if self.board.score > self.game_stats['best_score']:
            best_text = score_font.render("🏆 NEW BEST SCORE! 🏆", True, COLORS['gold'])
            best_rect = best_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80))
            self.screen.blit(best_text, best_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 36)  # Increased from 32
        instruction = instruction_font.render("Press R to restart", True, COLORS['neon_cyan'])
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 140))
        self.screen.blit(instruction, instruction_rect)
    
    def run(self):
        """Main game loop"""
        print("🚀 Starting Futuristic 2048...")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        # Save best score before exit
        if self.board.score > self.game_stats['best_score']:
            save_best_score(self.board.score)
        
        pygame.quit()
        print("👋 Thanks for playing!")

# ========================================
# BENCHMARK & ANALYSIS TOOLS
# ========================================

def run_benchmark(agent_name: str, num_games: int = 10, max_depth: int = 3) -> Dict:
    """
    Run automated benchmark for AI agents (AI: Performance evaluation)
    """
    print(f"\n🧪 Running benchmark: {agent_name} ({num_games} games)")
    
   
    
    scores = []
    win_2048 = 0
    total_moves = []
    
    for game_num in range(num_games):
        board = Board()
        moves = 0
        
        while board.can_move() and moves < 1000:  # Prevent infinite games
            if agent_name == "Greedy":
                move = greedy_agent(board)
            elif agent_name == "Expectimax":
                move = expectimax_agent(board, max_depth)
            else:
                continue
            
            if move:
                board.move(move)
                moves += 1
            else:
                break
        
        scores.append(board.score)
        total_moves.append(moves)
        
        # Check for 2048 tile
        max_tile = max(max(row) for row in board.grid)
        if max_tile >= 2048:
            win_2048 += 1
        
        print(f"  Game {game_num + 1}: Score {board.score}, Max tile {max_tile}, Moves {moves}")
    
    results = {
        'agent': agent_name,
        'num_games': num_games,
        'scores': scores,
        'avg_score': sum(scores) / len(scores),
        'max_score': max(scores),
        'min_score': min(scores),
        'win_rate_2048': win_2048 / num_games,
        'avg_moves': sum(total_moves) / len(total_moves)
    }
    
    print(f"\n📊 Results for {agent_name}:")
    print(f"   Average Score: {results['avg_score']:.1f}")
    print(f"   Max Score: {results['max_score']}")
    print(f"   2048 Win Rate: {results['win_rate_2048']:.1%}")
    print(f"   Average Moves: {results['avg_moves']:.1f}")
    
    return results

# ========================================
# ENTRY POINT
# ========================================

def main():
    """Main entry point"""
    # Check if benchmark mode requested
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "benchmark":
        print("🧪 BENCHMARK MODE")
        
        # Run benchmarks
        greedy_results = run_benchmark("Greedy", 10)
        expectimax_results = run_benchmark("Expectimax", 5, max_depth=2)
        
        # Save results
        benchmark_data = {
            'timestamp': time.time(),
            'greedy': greedy_results,
            'expectimax': expectimax_results
        }
        
        with open('benchmark_results.json', 'w') as f:
            json.dump(benchmark_data, f, indent=2)
        
        print("\n💾 Benchmark results saved to benchmark_results.json")
        
    else:
        # Normal game mode
        game = FuturisticGame2048()
        game.run()

if __name__ == "__main__":
    main()
