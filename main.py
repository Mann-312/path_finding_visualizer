import pygame
import math

from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finder")

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
YELLOW = [255, 255, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
PURPLE = [128, 0, 128]
ORANGE = [255, 165, 0]
GREY = [128, 128, 128]
TORQUOISE = [64, 224, 208]


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TORQUOISE

    def reset(self):
        self.color = WHITE

    def make_close(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TORQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current.make_path();
        current = came_from[current]
        draw();
    current.make_path()
    draw()


def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for it in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[it]:
                g_score[it] = temp_g_score
                came_from[it] = current
                f_score[it] = temp_g_score + h(it.get_pos(), end.get_pos());
                if it not in open_set_hash:
                    count += 1
                    open_set.put((f_score[it], count, it))
                    open_set_hash.add(it)
                    it.make_open()
        draw()

        if current != start:
            current.make_close()
    return False


def dijkstra(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    distance = {spot: float("inf") for row in grid for spot in row}
    distance[start] = 0
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_distance = distance[current] + h(neighbor.get_pos(), current.get_pos())
            if temp_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_distance
                if neighbor not in open_set_hash:
                    open_set.put((distance[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_close()

    return False


def BFS(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((count, start))
    came_from = {}
    visited = {spot: bool(False) for row in grid for spot in row}
    visited[start] = True
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if visited[neighbor] == False:
                came_from[neighbor] = current
                count += 1
                open_set.put((count, neighbor))
                visited[neighbor] = True
                neighbor.make_open()

        draw()

        if current != start:
            current.make_close()
    return False


def DFS(draw, grid, start, end):
    stack = []
    came_from = {}
    visited = {spot: bool(False) for row in grid for spot in row}
    current = start
    visited[current] = True
    while current != None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        dfs_flag = False
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        for neighbor in current.neighbors:
            if visited[neighbor] == False:
                stack.append(current)
                came_from[neighbor] = current
                current = neighbor
                visited[current] = True
                neighbor.make_open()
                dfs_flag = True
                break

        if dfs_flag == False:
            if len(stack) == 0:
                current = None
            else:
                current = stack[-1]
                stack.pop()
        if current != start:
            current.make_close()
        draw()
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    # pass
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()



            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None

                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                elif event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    BFS(lambda: draw(win, grid, ROWS, width), grid, start, end)
                elif event.key == pygame.K_c and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    DFS(lambda: draw(win, grid, ROWS, width), grid, start, end)
                elif event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                elif event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)