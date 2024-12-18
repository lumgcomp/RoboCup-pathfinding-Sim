RoboCup Pathfinding Simulation

This project demonstrates pathfinding algorithms in a RoboCup-inspired simulation environment. It allows users to visualise and compare the performance of different algorithms in navigating a player towards a ball while avoiding obstacles.

Getting Started

Prerequisites

Python: Install Python 3.11.0 or later.

Required Libraries:

pygame

numpy

Installation Steps

Download the Project

Download and unzip the project archive, titled 30011494-Diss-sim.

Open the Project

In PyCharm

Open PyCharm.

Click File (top-left menu) and select Open.

Navigate to the unzipped project folder and select it.

In VS Code

Open Visual Studio Code.

Click File > Open Folder and select the unzipped project folder.

Set Up Python Interpreter

In PyCharm

Go to File > Settings > Project: [Project Name] > Python Interpreter.

Click Add Interpreter and select Python 3.11.0.

In VS Code

Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS).

Search for and select Python: Select Interpreter.

Choose Python 3.11.0 from the list. If it is not listed, ensure Python 3.11.0 is installed on your system and added to your PATH.

Install Required Libraries

In PyCharm

Click the + sign in the Python Interpreter settings.

Search for and install the following libraries:

pygame

numpy

In VS Code

Open a terminal within VS Code (Ctrl+` or View > Terminal).

Run the following commands:

pip install pygame numpy

Ensure the terminal is using the correct Python interpreter by checking the interpreter displayed in the bottom-right corner of the VS Code window.

How to Use

Running the Simulation

Run the main script:

In PyCharm, click the Run button or select Run > Run... from the top menu.

In VS Code, open the main script and press F5 or click Run > Start Debugging.

Use the arrow keys to navigate the algorithm menu (top-right corner of the simulation window).

Select the algorithm you want to test.

Click Move to Ball to start the simulation.

Controls

Move to Ball: Start the simulation with the selected algorithm.

Reset: Resets the player and ball to their original positions, allowing comparison of algorithm performance on the same path.

Restart: Resets the game with new spawn points for the player, ball, and defenders.

Purpose

This program is designed to:

Visualize Pathfinding Algorithms: Show how different algorithms solve the pathfinding problem in real-time.

Enable Comparisons: Compare algorithm performance based on speed and efficiency in navigating a graph-based environment.

Notes

Ensure all dependencies are correctly installed for the program to function.

If you encounter issues with the interpreter, double-check that the correct Python version is selected and all required libraries are installed.
