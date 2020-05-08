Hello! This is a simple natural selection simulation with randomized mutations.  
The canvas uses tkinter, run main to begin (will start automatically).  
There are two classes of Bugs atm:  
- Bug: A base class for bugs, uses randomized mutation to jump certain distances in certain directions (doesnt pick up food it passes by). Hostile towards all classes.  
- IntelliBug: A child of Bug, but another Base Class to give other bugs path finding abilities; no randomized movements when possible.  
- Beetle: Similar to Naive, but walks instead of jumps; can pick up food in distance traveled path, but gets less energy from food. Hostile towards other classes, not self.  
- Fly: Flies around, cannot be hit by ground units while flying, but also cannot eat; base class for all flying units. 
- LowFly: Flies around, but can eat food while flying; higher energy costs than the fly.  
- DragonFly: Flies around, can attack units while flying. Special perk to ignore childhood immunity.  
- QueenAnt: Barely moves, high childhood immunity and initial energy, rarely respawns itself, but spawns worker ants at an insane rate.  
- WorkerAnt: Cannot reproduce, very weak unit that gives food back to its queen ant.  
- Tick: Unit that gets insane boosts off killing another unit. Special perk to avoid most attacks not started by itself.


Current randomized stats are:  
- Move Direction Probability  
- Move Direction Distance  
- Bug Strength
- Digestion
- Hostility
- Flying Chance (Flying Units Only)
- Fly Speed Boost (Flying Units Only)
- Birth Type Chances (Queen Bugs Only)
