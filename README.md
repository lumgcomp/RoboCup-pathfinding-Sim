# RoboCup Pathfinding Simulation

This project demonstrates pathfinding algorithms in a RoboCup-inspired simulation environment. It allows users to visualize and compare the performance of different algorithms in navigating a player towards a ball while avoiding obstacles.

The following algorithms are implemented:

- A*: A heuristic-based search algorithm that finds the shortest path efficiently by combining the advantages of Dijkstra's algorithm and Greedy Best-First Search. It uses a cost function to prioritize nodes based on distance from the start and estimated distance to the goal.

- Dijkstra's Algorithm: A classic algorithm that finds the shortest path from a source to all other nodes in a graph, prioritizing nodes based on accumulated cost without using heuristics.

- Depth-First Search (DFS): An uninformed search algorithm that explores as far as possible along a branch before backtracking. While not guaranteed to find the shortest path, it demonstrates how a brute-force approach can work in pathfinding.

- Breadth-First Search (BFS): An uninformed search algorithm that explores all neighbors at the current depth before moving deeper. It guarantees the shortest path in an unweighted graph.

- Ant Colony Optimization (ACO): A probabilistic optimization algorithm inspired by the behavior of ants finding paths to food. It uses pheromone trails to iteratively improve solutions to the pathfinding problem.
---

## Getting Started

### Prerequisites

- **Python**: Install Python 3.11.0 or later.
- **Required Libraries**:
  - `pygame`
  - `numpy`

### Installation Steps

1. **Download the Project**
   - Download and unzip the project archive, titled `30011494-Diss-sim`.

2. **Open the Project**

   #### In PyCharm
   - Open PyCharm.
   - Click **File** (top-left menu) and select **Open**.
   - Navigate to the unzipped project folder and select it.

   #### In VS Code
   - Open Visual Studio Code.
   - Click **File > Open Folder** and select the unzipped project folder.

3. **Set Up Python Interpreter**

   #### In PyCharm
   - Go to **File > Settings > Project: [Project Name] > Python Interpreter**.
   - Click **Add Interpreter** and select Python 3.11.0.

   #### In VS Code
   - Open the **Command Palette** (Ctrl+Shift+P or Cmd+Shift+P on macOS).
   - Search for and select **Python: Select Interpreter**.
   - Choose Python 3.11.0 from the list. If it is not listed, ensure Python 3.11.0 is installed on your system and added to your PATH.

4. **Install Required Libraries**

   #### In PyCharm
   - Click the **+** sign in the Python Interpreter settings.
   - Search for and install the following libraries:
     - `pygame`
     - `numpy`

   #### In VS Code
   - Open a terminal within VS Code (Ctrl+\` or View > Terminal).
   - Run the following commands:
     ```bash
     pip install pygame numpy
     ```
   - Ensure the terminal is using the correct Python interpreter by checking the interpreter displayed in the bottom-right corner of the VS Code window.

---

## How to Use

### Running the Simulation

1. Run the main script:
   - In PyCharm, click the **Run** button or select **Run > Run...** from the top menu.
   - In VS Code, open the main script and press **F5** or click **Run > Start Debugging**.

2. Use the **arrow keys** to navigate the algorithm menu (top-right corner of the simulation window).
   - Select the algorithm you want to test.
3. Click **Move to Ball** to start the simulation.

### Controls

- **Move to Ball**: Start the simulation with the selected algorithm.
- **Reset**: Resets the player and ball to their original positions, allowing comparison of algorithm performance on the same path.
- **Restart**: Resets the game with new spawn points for the player, ball, and defenders.

---

## Purpose

This program is designed to:

- **Visualize Pathfinding Algorithms**: Show how different algorithms solve the pathfinding problem in real-time.
- **Enable Comparisons**: Compare algorithm performance based on speed and efficiency in navigating a graph-based environment.

---

## Notes

- Ensure all dependencies are correctly installed for the program to function.
- If you encounter issues with the interpreter, double-check that the correct Python version is selected and all required libraries are installed.
