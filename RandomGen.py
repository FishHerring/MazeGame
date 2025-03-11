import pygame # Importerer pygame, som er et bibliotek til at lave spil.
from random import choice, randint # Importerer choice og randint fra random, som bruges i vores tilfælde til at vælge en tilfældig nabo til en celle, og en tilfældig slutposition for spilleren.


# Window settings
WIDTH, HEIGHT, TILE = 400, 400, 50 # Længde og bredde af vinduet, samt størrelsen af hver celle.
cols, rows = WIDTH // TILE, HEIGHT // TILE # Definerer cols og rows som længden og bredden af vinduet, og definerer størrelsen af hver celle.
BLUE, RED, GREEN = (0, 0, 255), (255, 0, 0), (0, 255, 0) # Farvekoder for spilleren, slutposition og startpositionen.

# Pygame setup
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT)) # Pygame funktion til at vise vinduet uf fra WIDTH og HEIGHT.
pygame.display.set_caption("Maze Game") # Spil Titel
clock = pygame.time.Clock() # FPS

class Cell: 
    def __init__(self, x, y): # Hver celle har en x og y koordinat, samt 4 vægge.
        self.x, self.y = x, y # x og y koordinaterne for cellen.
        self.walls = {side: True for side in ('top', 'right', 'bottom', 'left')} # Alle vægge er True som default.
        self.visited = False # Hvis cellen er besøgt eller ej.
    
    def draw(self, sc): # Funktion til at tegne cellen.
        x, y = self.x * TILE, self.y * TILE # x og y koordinaterne for cellen.
        if self.visited: # Hvis cellen er besøgt, så tegnes cellen sort.
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE)) # Tegner cell sort.
        for wall, coords in {'top': (x, y, x + TILE, y), 'right': (x + TILE, y, x + TILE, y + TILE), 
                             'bottom': (x, y + TILE, x + TILE, y + TILE), 'left': (x, y, x, y + TILE)}.items(): # Tegner væggene.
            if self.walls[wall]: # Hvis væggen er True, så tegnes væggen.
                pygame.draw.line(sc, pygame.Color('darkorange'), coords[:2], coords[2:], 2) # Tegner væggen.
    
    def check_neighbors(self, grid): # Funktion til at tjekke om cellen har naboer.
        neighbors = [(self.x + dx, self.y + dy) for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]] # Koordinater for naboer til cellen, og definerer dem som neighbors.
        unvisited = [grid[x + y * cols] for x, y in neighbors if 0 <= x < cols and 0 <= y < rows and not grid[x + y * cols].visited] # Tjekker om naboerne er besøgt eller ej, og definerer dem som unvisited.
        return choice(unvisited) if unvisited else None # Returnerer en tilfældig nabo, hvis der er nogen. (Vælges ud fra unvisited)


def remove_walls(a, b): # Funktion til at fjerne vægge mellem to celler.
    dx, dy = a.x - b.x, a.y - b.y # Definerer dx og dy som forskellen mellem cellerne.
    if dx == 1: a.walls['left'], b.walls['right'] = False, False # Hvis dx er 1, så fjernes væggen mellem cellerne.
    if dx == -1: a.walls['right'], b.walls['left'] = False, False # Hvis dx er -1, så fjernes væggen mellem cellerne.
    if dy == 1: a.walls['top'], b.walls['bottom'] = False, False # Hvis dy er 1, så fjernes væggen mellem cellerne.
    if dy == -1: a.walls['bottom'], b.walls['top'] = False, False # Hvis dy er -1, så fjernes væggen mellem cellerne.


def generate_maze(): # Funktion til at generere labyrinten.
    grid = [Cell(x, y) for y in range(rows) for x in range(cols)] # Opretter en liste med celler, ud fra x og y koordinaterne i cell og rows, og definerer dem som grid.
    stack, current = [], grid[0] # Stack er en tom liste, og current er den første celle i grid.
    current.visited, visited_count = True, 1 # Definerer current som besøgt, og visited_count som 1.
    while visited_count < len(grid): # Så længe visited_count er mindre end længden af grid.
        next_cell = current.check_neighbors(grid) # Definerer next_cell som nabo til current.
        if next_cell: # Hvis der er en nabo.
            next_cell.visited = True # Definerer next_cell som besøgt.
            stack.append(current) # Tilføjer current til stack.
            remove_walls(current, next_cell) # Fjerner væggen mellem current og next_cell.
            current, visited_count = next_cell, visited_count + 1 # Definerer current som next_cell, og visited_count som visited_count + 1.
        elif stack: # Hvis stack ikke er tom. 
            current = stack.pop() # pop er en funktion der fjerner det sidste element i en liste, her fjernes current fra stack.
    return grid # Returnerer grid, som er labyrinten.


def main(): # Main er funktionen der kører spillet.
    grid = generate_maze() # Genererer labyrinten, ud fra funktionen generate_maze.
    player_pos, end = [0, 0], [cols - 1, randint(0, rows - 1)] # Definerer player_pos som spillerens start position, altså i den første celle, samt end som en random position i højre siden af skærmen.
    running = True # Så længe spillet kører er running True.
    while running: # Så længe running er True.
        sc.fill(pygame.Color('gray20')) # Baggrunden er grå.
        for cell in grid: # For hver celle i grid.
            cell.draw(sc) # sc er vinduet, og cell.draw tegner cellen.
        pygame.draw.rect(sc, RED, (TILE * 0.15, TILE * 0.15, TILE * 0.7, TILE * 0.7)) # Tegner en rektangel, som har farven rød, og er spillerens start position.
        pygame.draw.rect(sc, GREEN, (end[0] * TILE + TILE * 0.15, end[1] * TILE + TILE * 0.15, TILE * 0.7, TILE * 0.7)) # Tegner en rektangel, som har farven grøn, og er spillerens slut position.
        pygame.draw.rect(sc, BLUE, (player_pos[0] * TILE + TILE//4, player_pos[1] * TILE + TILE//4, TILE//2, TILE//2)) # Tegner spilleren som blå, og placere dem ved player_pos, hvilket er start positionen, herefter tegnes spillerens størrelse.
        pygame.display.flip() # Opdaterer labyrinten med de nye ændringer.
        clock.tick(30) # Sætter vores FPS til 30.
        for event in pygame.event.get(): # Henter "events" fra spillet, altså såsom spillerens bevægelse.
            if event.type == pygame.QUIT: # Hvis spillet er slut
                running = False # Sæt running til false, altså stop spillet.
            elif event.type == pygame.KEYDOWN: # Hvis en knap trykkes ned.
                x, y = player_pos # definerer x og y som spillerens position.
                current_cell = grid[x + y * cols] # Henter den nuværende celle i labyrinten baseret på spillerens position.  
                # Tjekker om spilleren kan bevæge sig i en given retning, og om der er en mur i vejen
                if event.key == pygame.K_LEFT and x > 0 and not current_cell.walls['left']:
                    player_pos[0] -= 1 # Flytter spilleren til venstre
                elif event.key == pygame.K_RIGHT and x < cols - 1 and not current_cell.walls['right']:
                    player_pos[0] += 1 # Flytter spilleren til højre
                elif event.key == pygame.K_UP and y > 0 and not current_cell.walls['top']:
                    player_pos[1] -= 1 # Flytter spilleren op
                elif event.key == pygame.K_DOWN and y < rows - 1 and not current_cell.walls['bottom']:
                    player_pos[1] += 1 # Flytter spilleren ned
        
        # Tjekker om spilleren har nået slutpositionen
        if player_pos == end:
            running = False # Stopper spillet hvis spillerens position er det samme som end.
        
    pygame.quit() # Lukker Pygame.
    
if __name__ == "__main__": # Hvis filen bliver kørt direkte, så kører main-funktionen.
    main() # Kører main-funktionen.
