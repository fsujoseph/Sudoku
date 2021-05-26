# Sudoku

## Project Description

This is my Sudoku program and I added a few complexities that made it a fun and challenging project. Implementing a solver wasn't too difficiult, however generating unique and solvable Sudoku boards is. What I learned through my experimentation and research is that you can permutate a valid Sudoku board billions of different ways and still have a valid board, but it will be completely unrecognizable. This is what I did, using a source file of a select group of easy, medium, and hard puzzles and applying random permutations to keep a fresh experience for the user.

There are also more complex ways to generate boards without an already valid one; I tried to do that initially but was having trouble. It was only until after I finished the program I realized a small bug was messing up this attempt! I hope to re-visit that challenge in the future.

This project contains a GUI made with PyGame. There are options to start a new game, get a hint, or even listen to some relaxing tunes while you play. However the coolest part is if you press space you can watch the computer solve the board, and really see how the algorithm "thinks" which is really cool! I also paid particular attention to making sure the music still plays even if you start a new game, and that it will always play a different song, even if you turn the music off and turn it back on.

## Executing Program

To run script, download the folder and run the GUI script.

Press space to auto-solve and visualize the backtracking algorithm. I reccommend only doing this on the Easy difficulty as it is very time consuming on harder boards.

Due to Github's limit on file size, music file is limited. Feel free to download anything as a .wav file and place it in the music file.

## Future Improvements

In the future I may attempt to turn this into a web-app to try and test the skills I am learning now in class.
