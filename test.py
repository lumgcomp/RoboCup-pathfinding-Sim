import numpy as np
import random

# Define the grid
grid = np.array([
    [0, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

# Define the start and end points
start = (0, 0)
end = (5, 5)


# Define the ant colony optimization algorithm
def ant_colony_optimization(grid, start, end, num_ants=10, num_iterations=100, alpha=1, beta=2, evaporation_rate=0.5,
                            pheromone_deposit=10):
    # Initialize the pheromone matrix
    pheromone = np.zeros_like(grid, dtype=float)
    pheromone[start] = 1

    # Run the ant colony optimization algorithm for the specified number of iterations
    for iteration in range(num_iterations):
        # Initialize the ant positions
        ants = [start] * num_ants

        # Move the ants toward the end point
        for ant in ants:
            if ant == end:
                continue

            # Determine the next move based on the pheromone and heuristic information
            possible_moves = []
            for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (ant[0] + move[0], ant[1] + move[1])
                if 0 <= next_pos[0] < grid.shape[0] and 0 <= next_pos[1] < grid.shape[1] and grid[next_pos] == 0:
                    possible_moves.append(next_pos)

            if len(possible_moves) == 0:
                continue

            probabilities = np.array(
                [pheromone[next_pos] ** alpha * (1.0 / (1.0 + grid[next_pos]) ** beta) for next_pos in possible_moves])
            probabilities /= np.sum(probabilities)
            next_pos = possible_moves[np.random.choice(len(possible_moves), p=probabilities)]
            ants[ants.index(ant)] = next_pos

            # Deposit pheromone on the path
            pheromone[ant] *= evaporation_rate
            pheromone[next_pos] += pheromone_deposit

        # Check if any of the ants reached the end point
        if end in ants:
            break

    # Construct the path from the pheromone matrix
    path = [end]
    while path[-1] != start:
        possible_moves = []
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (path[-1][0] + move[0], path[-1][1] + move[1])
            if 0 <= next_pos[0] < grid.shape[0] and 0 <= next_pos[1] < grid.shape[1] and grid[next_pos] == 0:
                possible_moves.append(next_pos)
        probabilities = np.array([pheromone[next_pos] for next_pos in possible_moves])
        # Check if any of the ants reached the end point
        if end in ants:
            break

    # Construct the path from the pheromone matrix
    path = [end]
    while path[-1] != start:
        possible_moves = []
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (path[-1][0] + move[0], path[-1][1] + move[1])
            if 0 <= next_pos[0] < grid.shape[0] and 0 <= next_pos[1] < grid.shape[1] and grid[next_pos] == 0:
                possible_moves.append(next_pos)
        probabilities = np.array(
            [pheromone[next_pos] ** alpha * (1.0 / (1.0 + grid[next_pos]) ** beta) for next_pos in possible_moves])
        next_pos = possible_moves[np.argmax(probabilities)]
        path.append(next_pos)

    # Return the path
    return path[::-1]


if __name__ == '__main__':
    # Print the path
    path = ant_colony_optimization(grid, start, end)
    print(path)
