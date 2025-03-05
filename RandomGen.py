import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# Generate maze walls with values
walls = []
for row in range(ROWS + 1):
    for col in range(COLS + 1):
        if random.choice([True, False]):  # Randomly place walls
            walls.append(((col * CELL_SIZE, row * CELL_SIZE), random.randint(1, 10)))

def draw_maze():
    screen.fill(WHITE)
    for wall, value in walls:
        pygame.draw.rect(screen, BLACK, (*wall, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def destroy_random_wall():
    if walls:
        walls.pop(random.randint(0, len(walls) - 1))

def main():
    running = True
    while running:
        draw_maze()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    destroy_random_wall()
        clock.tick(10)
    pygame.quit()

if __name__ == "__main__":
    main()