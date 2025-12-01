# Harvest-Heights

Harvest Heights is a 2D platformer game project developed to practice and test our game development skills. The game was made for the class CCOM 4440: Python (Introduction to Videogames) at the University of Puerto Rico at Arecibo.

As the name class name implies, the project game was developed fully in python. It was made using free sprites, assets, and sounds on itch.io.

## How to Run
Run the main.py file to play the game.

## Controls
* Use the Arrow keys to move left and right.
* Use the Spacebar to jump
* Use the ESC key to pause the game

## Known Issues
* On level screens beyond the first screen, the Trunk enemy turns to face away from the player when starting the screen and turn back to resume its intended behavior. The decision was made to not fix this issue as one of the developers thought it added a sort of charm to the enemy.
* Due to the nature of the sprites transparent area, most notably Trunk's sprites, it causes the enemies to not collide fully with the terrain, either stopped by an apparent invisible barrier or walking on mid-air until the sprite's rectangle moves off the platform completely. Attempts to fix this issue cause sprites to jitter and teleport around.

## Contributions
**Kartanien**
* Project Idea and Proposal
* Player and Enemy Movement
* Start Screen
* Level Design
* Motivator (without him, the other contributor would have lazed around and done nothing)
* Pause State and Menu

**Efrain**
* Asset Selection
* Animations
* Collisions
* Level, Scene, and Start Screen Builders
* Collectables
* Sprite Interactions
* Game Over Screen and its Interactions

## Individual Reflections