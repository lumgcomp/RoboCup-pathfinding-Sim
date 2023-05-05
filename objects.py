import heapq
import math
import random

import numpy as np
import pygame.sprite
from constants import *


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, win):
        win.blit(self.image, self.rect)


class Pitch(MySprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.grid_size = 10,10
        self.grid = np.zeros(self.grid_size, dtype=int)

    def draw(self, win, draw_grid=True):
        win.blit(self.image, self.rect)
        if draw_grid:
            n, m = self.grid_size
            for i in range(n):
                pygame.draw.line(win, WHITE, (i * WIDTH // n, 0), (i * WIDTH // n, HEIGHT))
            for j in range(m):
                pygame.draw.line(win, WHITE, (0, j * HEIGHT // m), (WIDTH, j * HEIGHT // m))

    def add_ennemy(self, i, j):
        self.grid[i, j] = 1

    def remove_ennemy(self, i, j):
        self.grid[i, j] = 0


class Ball(MySprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def init_random_position(self, pitch: Pitch):
        n, m = pitch.grid_size
        self.rect.center = (random.randint(0, n - 1) * WIDTH // n + WIDTH // n // 2,
                            random.randint(0, m - 1) * HEIGHT // m + HEIGHT // m // 2)


class Player(MySprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.path = None  # list of points ex. [(170, 200), (180, 210), (190, 220), (200, 230), (210, 240)]

    def find_path_to(self, destination_obj: pygame.sprite.Sprite, pitch: Pitch, algo: str):
        """
        Find the path to the destination object and store it in self.path
        :param destination_obj:
        :param pitch:
        :param algo: "a_star", "dijkstra", "dfs", "bfs", "rrt", "aca"
        return: None
        """

        n, m = pitch.grid_size
        case_size = WIDTH // n, HEIGHT // m
        i_player, j_player = self.rect.center[1] // case_size[1], self.rect.center[0] // case_size[0]
        i_ball, j_ball = destination_obj.rect.center[1] // case_size[1], destination_obj.rect.center[0] // case_size[0]

        start, end = (i_player, j_player), (i_ball, j_ball)

        print(f"start: {start}, end: {end}")
        print(pitch.grid)

        path = fonction_dico[algo](start, end, pitch.grid)

        self.path = [(j * case_size[0] + case_size[0] // 2, i * case_size[1] + case_size[1] // 2) for i, j in path]

    def update(self, dt):
        if self.path:
            destination = self.path[0]
            if self.rect.center == destination:
                self.path.pop(0)
            else:
                self.move_to(destination, dt)

    def move_to(self, destination, dt):
        x, y = self.rect.center
        dx, dy = destination[0] - x, destination[1] - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        speed = 200
        if distance > 0:
            max_distance = speed * dt / 1000
            if distance <= max_distance:
                self.rect.center = destination
            else:
                _ratio = max_distance / distance
                self.rect.center = x + dx * _ratio, y + dy * _ratio

    def init_random_position(self, pitch: Pitch):
        n, m = pitch.grid_size
        self.rect.center = (random.randint(1, n - 2) * WIDTH // n + WIDTH // n // 2,
                            random.randint(0, m - 2) * HEIGHT // m + HEIGHT // m // 2)

    def draw(self, win, draw_path=True):
        super().draw(win)
        if draw_path:
            if self.path:
                for i in range(len(self.path)):
                    x, y = self.path[i]
                    pygame.draw.circle(win, RED, (x, y), 5)


class Ennemy(MySprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.i = 0
        self.j = 0

    def init_random_position(self, pitch: Pitch):
        n, m = pitch.grid_size
        j = random.randint(1, n - 2)
        i = random.randint(0, m - 2)
        self.i = i
        self.j = j
        self.rect.center = (j * WIDTH // n + WIDTH // n // 2,
                            i * HEIGHT // m + HEIGHT // m // 2)


def a_star(start, end, grid) -> list[tuple[int, int]]:
    """
    grid is a list of lists of 0 or 1 (0 = free, 1 = obstacle)
    """

    # define heuristic function to estimate distance to goal
    def heuristic(a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    n, m = len(grid), len(grid[0])
    # define possible movements (up, down, left, right, diagonal)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # create set of visited nodes and heap queue for exploring nodes
    visited = set()
    heap = [(0, start)]
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    c = 0
    # loop until heap queue is empty or goal is reached
    while heap:
        c += 1
        # get node with the lowest cost from heap queue
        current_cost, current_node = heapq.heappop(heap)

        # check if goal is reached
        if current_node == end:
            break

        # check neighbors of current node
        for i, j in neighbors:
            neighbor = current_node[0] + i, current_node[1] + j
            ni, nj = neighbor

            # skip neighbor if it is outside the grid
            if ni < 0 or ni >= n or nj < 0 or nj >= m:
                continue

            new_cost = cost_so_far[current_node] + grid[ni][nj]

            # skip neighbor if it is not traversable or has already been visited
            if neighbor in visited or grid[ni][nj] == 1:
                continue

            # update cost and add neighbor to heap queue
            cost_so_far[neighbor] = new_cost
            priority = new_cost + heuristic(end, neighbor)
            heapq.heappush(heap, (priority, neighbor))
            visited.add(neighbor)
            came_from[neighbor] = current_node

    # build path from start to end using came_from dictionary
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def get_neighbors(node, grid):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    x, y = node
    if x > 0 and grid[x - 1][y] == 0:
        neighbors.append((x - 1, y))
    if x < rows - 1 and grid[x + 1][y] == 0:
        neighbors.append((x + 1, y))
    if y > 0 and grid[x][y - 1] == 0:
        neighbors.append((x, y - 1))
    if y < cols - 1 and grid[x][y + 1] == 0:
        neighbors.append((x, y + 1))
    return neighbors


def dfs(start, end, grid):
    """
    grid is a list of lists of 0 or 1 (0 = free, 1 = obstacle)
    """

    stack = [start]
    visited = set()
    parent = {}
    while stack:
        node = stack.pop()
        if node == end:
            path = []
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            return path
        if node in visited:
            continue
        visited.add(node)
        for neighbor in get_neighbors(node, grid):
            if neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = node
    return []


from collections import deque


def bfs(start, end, grid):
    """
    grid is a list of lists of 0 or 1 (0 = free, 1 = obstacle)
    """
    queue = deque([start])
    visited = set()
    parent = {}
    while queue:
        node = queue.popleft()
        if node == end:
            path = []
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            return path
        if node in visited:
            continue
        visited.add(node)
        for neighbor in get_neighbors(node, grid):
            if neighbor not in visited:
                queue.append(neighbor)
                parent[neighbor] = node
    return []


import heapq


def dijkstra(start, end, grid):
    """
    grid is a list of lists of 0 or 1 (0 = free, 1 = obstacle)
    """
    heap = [(0, start)]
    visited = set()
    dist = {start: 0}
    parent = {}
    while heap:
        (d, node) = heapq.heappop(heap)
        if node == end:
            path = []
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            return path
        if node in visited:
            continue
        visited.add(node)
        for neighbor in get_neighbors(node, grid):
            new_dist = dist[node] + 1
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
                parent[neighbor] = node
    return []


def aca(start, end, real_grid):
    """Grid must be a square to run ant algo (because this ant algo is bad)"""
    import aco_folder.aco.ant_colony as ac
    import aco_folder.aco.map_class as mp

    # grid is like real grid but its shape is a square
    grid = []
    nb_lines = len(real_grid)
    for i in range(nb_lines):
        grid.append(real_grid[i][:nb_lines])

    print(grid)

    ants = 10
    iterations = 100
    p = 0.1
    Q = 1
    np_grid = np.array(grid)
    for i in range(len(np_grid)):
        for j in range(len(np_grid[0])):
            if np_grid[i][j] == 0:
                np_grid[i][j] = 1
            else:
                np_grid[i][j] = 0
    mapp = mp.Map(np_grid, start, end)
    colony = ac.AntColony(mapp, ants, iterations, p, Q)
    path = colony.calculate_path()
    return path


fonction_dico = {"a_star": a_star, "dijkstra": dijkstra, "dfs": dfs, "bfs": bfs, "aca": aca}
