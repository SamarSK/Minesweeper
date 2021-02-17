# Minesweeper
## Introduction
This Python program imitates the classic Minesweeper game. The game has 3 difficulties and a "hint" option. 
## Prerequisites
Libraries: tkinter, random
## How to play
After the start of the program, a window with difficulties shows up and the game itself stars by choosing one of them (easy, medium or hard).

Goal of the game is to uncover all the squares without mines and to "flag" all the mines. (win condition)

A square can be uncovered by left-clicking on it with mouse cursor.
A square can be (un)flagged by right-clicking on it with mouse cursor.
A hint can be used by pressing key "H" on the keyboard while on a square with mouse cursor. If there is mine on a square, a red "!" shows up on a square for a short time, otherwise a green "✓" shows up.

The first left click always uncovers a square without a mine.
If a square with mine is uncovered, the game ends and restart is necessary.

Above the squares is a flag counter (red text) and a hint counter (green text).

The game can be restarted at any time by clicking on one of the difficulty buttons.

