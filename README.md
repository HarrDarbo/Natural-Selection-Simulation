Hello! This is a simple natural selection simulation with randomized mutations.  
The canvas uses tkinter, run main to begin (will start automatically).  
There are two classes of Bugs atm:  
- BugNaive: A base class for bugs, uses randomized mutation to jump certain distances in certain directions (doesnt pick up food it passes by). Hostile towards all classes.  
- BugGround: Similar to Naive, but walks instead of jumps; can pick up food in distance traveled path, but gets less energy from food. Hostile towards other classes, not self.  

Current randomized stats are:  
- Move Direction Probability  
- Move Direction Distance  
- Bug Strength
