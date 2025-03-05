import pygame
from random import choice

# Smaller Window
WIDTH, HEIGHT, TILE = 402, 402, 50
cols, rows = WIDTH // TILE, HEIGHT // TILE  
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {side: True for side in ('top', 'right', 'bottom', 'left')}
        self.visited = False

    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))

        directions = {'top': (x, y, x + TILE, y), 'right': (x + TILE, y, x + TILE, y + TILE),
                      'bottom': (x, y + TILE, x + TILE, y + TILE), 'left': (x, y, x, y + TILE)}

        for wall, coords in directions.items():
            if self.walls[wall]:
                pygame.draw.line(sc, pygame.Color('darkorange'), coords[:2], coords[2:], 2)

    def check_neighbors(self, grid_cells):
        neighbors = [self._get_cell(dx, dy, grid_cells) for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]]
        unvisited = [n for n in neighbors if n and not n.visited]
        return choice(unvisited) if unvisited else None

    def _get_cell(self, dx, dy, grid_cells):
        x, y = self.x + dx, self.y + dy
        return grid_cells[x + y * cols] if 0 <= x < cols and 0 <= y < rows else None


def remove_walls(a, b):
    dx, dy = a.x - b.x, a.y - b.y
    if dx == 1: a.walls['left'], b.walls['right'] = False, False
    if dx == -1: a.walls['right'], b.walls['left'] = False, False
    if dy == 1: a.walls['top'], b.walls['bottom'] = False, False
    if dy == -1: a.walls['bottom'], b.walls['top'] = False, False


def generate_maze():
    grid = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current, stack = grid[0], []
    visited_count = 1

    while visited_count < len(grid):
        current.visited = True
        next_cell = current.check_neighbors(grid)
        if next_cell:
            next_cell.visited = True
            visited_count += 1
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
        elif stack:
            current = stack.pop()

    return grid

def main():
    grid_cells = generate_maze()
    player_pos = [0, 0]
    end = [cols - 1, rows - 1]

    running = True
    while running:
        sc.fill(pygame.Color('gray20'))  # Background color
        for cell in grid_cells:
            cell.draw(sc)

        pygame.draw.rect(sc, BLUE, (player_pos[0] * TILE, player_pos[1] * TILE, TILE, TILE))
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                current_cell = grid_cells[player_pos[0] + player_pos[1] * cols]  # Get current cell
                
                if event.key == pygame.K_LEFT and player_pos[0] > 0 and not current_cell.walls['left']:
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and player_pos[0] < cols - 1 and not current_cell.walls['right']:
                    player_pos[0] += 1
                elif event.key == pygame.K_UP and player_pos[1] > 0 and not current_cell.walls['top']:
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and player_pos[1] < rows - 1 and not current_cell.walls['bottom']:
                    player_pos[1] += 1
                    
        if player_pos == end:
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
