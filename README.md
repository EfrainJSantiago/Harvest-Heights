# Harvest-Heights

Harvest Heights is a 2D platformer game project developed to practice and test our game development skills. The game was made for the class CCOM 4440: Python (Introduction to Videogames) at the University of Puerto Rico at Arecibo.

As the class name implies, the project game was developed fully in python. It was made using free sprites, assets, and sounds on itch.io.

The ZIP package download for this project can be found here: [https://github.com/EfrainJSantiago/Harvest-Heights](https://github.com/EfrainJSantiago/Harvest-Heights)

## How to Run
Run the main.py file to play the game.

## Controls
* Use the Arrow keys to move left and right.
* Use the Spacebar to jump
* Use the ESC key to pause the game

## Known Issues
* On level screens beyond the first screen, the Trunk enemy turns to face away from the player when starting the screen and turn back to resume its intended behavior. The decision was made to not fix this issue as one of the developers thought it added a sort of charm to the enemy.
* Due to the nature of the sprites transparent area, most notably Trunk's sprites, it causes the enemies to not collide fully with the terrain, either stopped by an apparent invisible barrier or walking on mid-air until the sprite's rectangle moves off the platform completely. Attempts to fix this issue cause sprites to jitter and teleport around.
* One of the collaborators, Kartanien, was unable to clone the project's GitHub repository due to unknown technical issues. Because of this, only the other collaborator, Efrain, could update the project repository. Any files and changes made by Kartanien had to go through Efrain to be reviewed and uploaded onto the repository.
* Probing enemies (Mushroom and Slime) have an issue where if they hit a wall while on a surface, they break. This problem doesn't show when hitting the screen edges.

## Contributions
**Kartanien**
* Project Idea and Proposal
* Player and Enemy Movement
* Start Screen
* Motivator (without him, the other contributor would have lazed around and done nothing)
* Decision Making
* Pause State and Menu
* Level Design
* Game Producer

**Efrain**
* Asset Selection
* Animations
* Collisions
* Level, Scene, and Start Screen Builders
* Collectables
* Game Over Screen and its Interactions
* Progression Implementation
* Sound Implementation
* Level Design

## Credits
* SPRITES by Pixel Frog - [(https://pixelfrog-assets.itch.io/pixel-adventure-1)](https://pixelfrog-assets.itch.io/pixel-adventure-1)
* ENEMIES by Pixel Frog - [(https://pixelfrog-assets.itch.io/pixel-adventure-2)](https://pixelfrog-assets.itch.io/pixel-adventure-2)
* SOUNDS by Kronbits - [(https://kronbits.itch.io/freesfx)](https://kronbits.itch.io/freesfx)
* MUSIC by Tallbeard Studios - [(https://tallbeard.itch.io/music-loop-bundle)](https://tallbeard.itch.io/music-loop-bundle)
* FONTS by Yūki Pixels - [(https://yukipixels.itch.io/boldpixels)](https://yukipixels.itch.io/boldpixels)

* SPRITE SHEET LOADING and ANIMATION CODE BASIS by freeCodeCamp.org - [(https://www.youtube.com/watch?v=6gLeplbqtqg)](https://www.youtube.com/watch?v=6gLeplbqtqg)