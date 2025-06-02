# Fleabag VS Mutt

A Python recreation of the classic Flash game where a teal cat (Fleabag) and a gray dog (Mutt) throw objects at each other over a fence.

## Features

- **Single Player Mode**: Play as Mutt against CPU-controlled Fleabag
- **Two Player Mode**: Local multiplayer (planned for future update)
- **Physics-based Gameplay**: Realistic projectile physics with wind effects
- **Special Powers**: Four unique power-ups for each character
- **Multiple Difficulty Levels**: Beginner, Average, and Hardcore AI

## Controls

### Basic Controls
- **Arrow Keys (Up/Down)**: Adjust throwing angle
- **Spacebar**: Hold to charge power, release to fire
- **Mouse**: Click power buttons to activate abilities

### Power-ups (Keys 1-4)
1. **Double Throw (x2)**: Fire two projectiles at once
2. **Power Up (Red)**: Bigger, more powerful projectile
3. **Stink Bomb (Yellow)**: Projectile becomes a smelly dead fish (extra damage)
4. **Heal (Green)**: Restore health

## Game Mechanics

### Characters
- **Mutt (Gray Dog)**: Throws bones, controlled by player
- **Fleabag (Teal Cat)**: Throws cans, CPU or second player controlled

### Gameplay
- Each character starts with 100 health
- Direct hits deal 15 damage (25 with power-up, +10 for stink bomb)
- Wind affects projectile trajectory
- Characters laugh when opponent misses
- First to reduce opponent's health to 0 wins

### Powers
- Each power can only be used once per round
- Powers reset after game over
- Strategic power usage is key to victory

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Technical Details

- Built with Python and Pygame
- 60 FPS gameplay
- Modular code structure for easy expansion
- Physics simulation includes gravity and wind resistance

## Future Enhancements

- [ ] Custom sprites and animations
- [ ] Sound effects and background music
- [ ] Menu system with difficulty selection
- [ ] Improved AI with personality differences
- [ ] Tournament mode
- [ ] Online multiplayer support
- [ ] Custom backgrounds and themes

## Assets Folder Structure

The game is designed to support custom assets:
- `assets/images/backgrounds/` - Background images
- `assets/images/characters/` - Character sprites
- `assets/images/projectiles/` - Projectile sprites
- `assets/sounds/effects/` - Sound effects
- `assets/sounds/music/` - Background music
- `assets/fonts/` - Custom fonts

## Contributing

Feel free to contribute by:
- Adding custom sprites and animations
- Implementing sound effects
- Improving AI behavior
- Adding new power-ups
- Creating new game modes

## License

This project is a fan recreation for educational purposes. Original game concept belongs to gametuner.com.