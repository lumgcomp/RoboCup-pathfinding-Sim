import numpy as np
import random

# Set random seed for reproducibility
random.seed(42)


class ACA:
    def __init__(self, grid, start, end, ant_count=10, max_iterations=100, alpha=1.0, beta=2.0, rho=0.1, Q=1.0):
        self.grid = grid
        self.start = start
        self.end = end
        self.ant_count = ant_count
        self.max_iterations = max_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.pheromone_grid = np.zeros_like(grid, dtype=float)
        self.best_path = None
        self.best_path_length = np.inf

    def run(self):
        for i in range(self.max_iterations):
            paths = self._generate_ant_paths()
            self._update_pheromones(paths)
            self._update_best_path(paths)

    def _generate_ant_paths(self):
        paths = []
        for ant in range(self.ant_count):
            path = self._generate_ant_path()
            paths.append(path)
        return paths

    def _generate_ant_path(self):
        current = self.start
        path = [current]
        while current != self.end:
            # Compute the probabilities for the ant to move to each neighbor cell
            prob = self._compute_transition_probabilities(current, path)
            # Choose the next cell based on the probabilities
            next_cell = self._choose_next_cell(prob)
            path.append(next_cell)
            current = next_cell
        return path

    def _compute_transition_probabilities(self, current, path):
        row, col = current
        # Get the valid neighbors of the current cell
        neighbors = self._get_neighbors(current)
        # Remove visited cells from the neighbors list
        neighbors = [n for n in neighbors if n not in path]
        # If there are no valid neighbors, return an array of zeros
        if not neighbors:
            return np.zeros(len(self.grid))
        # Compute the probability of choosing each neighbor cell
        prob = []
        total = 0.0
        for neighbor in neighbors:
            row_n, col_n = neighbor
            pheromone = self.pheromone_grid[row_n, col_n]
            distance = self._compute_distance(current, neighbor)
            # Use the distance and pheromone information to compute the probability
            p = (pheromone ** self.alpha) * ((1.0 / distance) ** self.beta)
            prob.append(p)
            total += p
        # Normalize the probabilities to sum up to 1
        prob = np.array(prob) / total
        return prob

    def _choose_next_cell(self, prob):
        # Choose the next cell based on the probabilities
        r = random.uniform(0.0, 1.0)
        accum = 0.0
        for i, p in enumerate(prob):
            accum += p
            if accum >= r:
                return self._get_neighbors(self.start)[i]
        return None

    def _get_neighbors(self, cell):
        row, col = cell
        # Define the offsets for the neighbor cells
        offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # Compute the coordinates of the
        # Compute the coordinates of the neighbor cells
        neighbors = []
        for offset in offsets:
            row_n = row + offset[0]
            col_n = col + offset[1]
            if 0 <= row_n < self.grid.shape[0] and 0 <= col_n < self.grid.shape[1]:
                if self.grid[row_n, col_n] == 0:
                    neighbors.append((row_n, col_n))
        return neighbors

    def _compute_distance(self, cell1, cell2):
        row1, col1 = cell1
        row2, col2 = cell2
        # Compute the Euclidean distance between two cells
        distance = np.sqrt((row2 - row1) ** 2 + (col2 - col1) ** 2)
        return distance

    def _update_pheromones(self, paths):
        # Evaporate the pheromones on all grid cells
        self.pheromone_grid *= (1.0 - self.rho)
        # Add pheromones to the grid cells visited by the ants
        for path in paths:
            length = self._compute_path_length(path)
            for i in range(len(path) - 1):
                row1, col1 = path[i]
                row2, col2 = path[i + 1]
                self.pheromone_grid[row1, col1, row2, col2] += self.Q / length

    def _update_best_path(self, paths):
        for path in paths:
            length = self._compute_path_length(path)
            if length < self.best_path_length:
                self.best_path = path
                self.best_path_length = length

    def _compute_path_length(self, path):
        length = 0.0
        for i in range(len(path) - 1):
            cell1 = path[i]
            cell2 = path[i + 1]
            length += self._compute_distance(cell1, cell2)
        return length
