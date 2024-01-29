###############################################################################
# Falling Sand Simulator                                                      #
#                                                                             #
# Inspired by The Coding Train's video on the same topic.                     #
# https://www.youtube.com/watch?v=L4u7Zy_b868                                 #
#                                                                             #
# Author: Laura O'Connor                                                      #
# Date Created: 2024/1/30                                                     #
###############################################################################

import pygame
import time
import numpy as np

# WINDOW_WIDTH_AND_HEIGHT and GRID_SIZE must be multiples of each other.
WINDOW_WIDTH_AND_HEIGHT = 560
GRID_SIZE = 80
SAND_SIZE = WINDOW_WIDTH_AND_HEIGHT // GRID_SIZE

# Colours are represented as HSLA values, with the exception of 0 which
# represents an empty cell. Single values represent hue.
DEFAULT_GRID_COLOUR = 0
DEFAULT_SAND_COLOUR = 5
ORIGINAL_SAND_COLOUR_RBG = (250, 170, 50)
DEFAULT_SAND_COLOUR = [0, 55, 66, 100]

# Speed settings.
TICK_RATE = 60
SPAWN_RATE_PER_SECOND = 20
COLOUR_CHANGE_SPEED = 0.015

grid = [[DEFAULT_GRID_COLOUR for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

last_spawn_time = 0
colour = 1
sand_colour = pygame.Color(ORIGINAL_SAND_COLOUR_RBG)

def main():
    pygame.init()
    pygame.display.set_caption("Falling Sand Simulator")
    screen = pygame.display.set_mode((WINDOW_WIDTH_AND_HEIGHT, WINDOW_WIDTH_AND_HEIGHT))
    clock = pygame.time.Clock()
    is_game_running = True

    while is_game_running:
        clock.tick(TICK_RATE)

        for event in pygame.event.get():                
            if event.type == pygame.QUIT:
                is_game_running = False
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
                is_game_running = False
        
        screen.fill((0, 0, 0))

        game_logic(screen)

        pygame.display.flip()
        

def game_logic(screen: pygame.surface) -> None:
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] < WINDOW_WIDTH_AND_HEIGHT and mouse_pos[1] < WINDOW_WIDTH_AND_HEIGHT and mouse_pos[0] > 0 and mouse_pos[1] > 0:
            if (grid[mouse_pos[0] // SAND_SIZE][mouse_pos[1] // SAND_SIZE]) == DEFAULT_GRID_COLOUR:
                global last_spawn_time

                if time.time() - last_spawn_time > 1 / SPAWN_RATE_PER_SECOND and pygame.mouse.get_pressed()[0]:
                    grid[mouse_pos[0] // SAND_SIZE][mouse_pos[1] // SAND_SIZE] = colour
                    last_spawn_time = time.time()

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] != DEFAULT_GRID_COLOUR:                
                sand_colour.hsla = (grid[i][j], DEFAULT_SAND_COLOUR[1], DEFAULT_SAND_COLOUR[2], DEFAULT_SAND_COLOUR[3])

                pygame.draw.rect(
                    surface=screen,
                    color=sand_colour,
                    rect=(i * SAND_SIZE, j * SAND_SIZE, SAND_SIZE, SAND_SIZE),
                    width=0
                )

    def move_sand(i, j):
        if j + 1 < GRID_SIZE:
            global colour

            # 360 is the maximum value for hue, and 0 here repsents an empty 
            # cell.
            if colour > 359:
                colour = 1

            if grid[i][j] != DEFAULT_GRID_COLOUR:
                if grid[i][j + 1] == DEFAULT_GRID_COLOUR:
                    grid[i][j] = DEFAULT_GRID_COLOUR
                    grid[i][j + 1] = colour
                    colour += COLOUR_CHANGE_SPEED

                elif grid[i][j + 1] != DEFAULT_GRID_COLOUR:
                    options = []

                    if i - 1 >= 0 and grid[i - 1][j + 1] == DEFAULT_GRID_COLOUR:
                        options.append(-1)
                    if i + 1 < GRID_SIZE and grid[i + 1][j + 1] == DEFAULT_GRID_COLOUR:
                        options.append(1)
                    
                    if len(options) == 0:
                        return
                    
                    sand_direction = np.random.choice(options)

                    if sand_direction == 0:
                        grid[i][j] = colour
                        colour += COLOUR_CHANGE_SPEED

                    else:
                        grid[i][j] = DEFAULT_GRID_COLOUR
                        grid[sand_direction + i][j + 1] = colour
                        colour += COLOUR_CHANGE_SPEED
    
    for i in range(GRID_SIZE):
        for j in range(0, GRID_SIZE, 2):
            move_sand(i, j)              

    for i in range(GRID_SIZE):
        for j in range(1, GRID_SIZE, 2):
            move_sand(i, j)
 

if __name__ == "__main__":
    main()