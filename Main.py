import pygame
import random
from Player_Class import *
from Grid_Class import Grid
from Settings import *


all_grid_objects = []
player_white = None
player_black = None
def add_object(color,grid, object_type, x, y):
    """
    Attempt to add an object to grid

    The steps are as follows:

    (1) Verify that the position specified by the x & y coordinates is empty in the grid. If not, exit.
    (2) Create a new object of type 'object_type' and set its position to the supplied x and y coordinates.
    (3) Add the new object to the all_grid_objects list.
    (4) Store a reference to the new object in the correct grid position
    :param grid: a grid to store grid objects
    :param object_type: the class of the new object to create
    :param x: the x coordinate to add the object to
    :param y: the y coordinate to add the object to
    """
    if grid.get(x,y) != None:
        return add_object(color,grid, object_type, random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
        
    
    else:
        new_obj = object_type(color,grid,x,y)
        
    all_grid_objects.append(new_obj)

    grid.set(x,y, new_obj)
    return all_grid_objects[-1]

def remove_object(grid, x, y):
    """
    Attempt to remove an object from grid

    The steps are as follows:

    (1) Verify that there is a particle of some kind in the specified position. If not, exit.
    (2) Remove the reference to the object from the grid.
    (3) Remove the object from the all_grid_objects list.
    :param grid: a grid to store grid objects
    :param x: the x coordinate to remove the object from
    :param y: the y coordinate to remove the object from
    """
    if grid.get(x,y) == None:
        return
    else:
        grid_ref = grid.get(x,y)
        grid.set(x,y, None)
        all_grid_objects.remove(grid_ref)
    return


def draw_grid(screen, grid):
    """
    Draws the grid on the screen.
    """
    for y in range(grid.height):
        for x in range(grid.width):
            rect = pygame.Rect(x * HORIZONTAL_SPACING + GRID_OFFSET_X, y * VERTICAL_SPACING + GRID_OFFSET_Y, HORIZONTAL_SPACING, VERTICAL_SPACING)
            # pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Draw grid lines
            # pygame.draw.circle(screen, (0, 0, 0), (rect.x + rect.width / 2, rect.y + rect.height / 2), 3)  # Draw grid centers
            # Check if there is a player at this grid position
            if grid.get(x, y) is not None:
                screen.blit(grid.get(x, y).image, (rect.x, rect.y))  # Draw player images

def main_loop(grid, screen, clock):
    input_combo_black = []
    input_combo_white = []
    player_black = all_grid_objects[0]
    player_white = all_grid_objects[1]
    flag_black = all_grid_objects[2]
    flag_white = all_grid_objects[3]
    goal_black = all_grid_objects[4]
    goal_white = all_grid_objects[5]
    game_on = True

    SCORE_LIMIT = int(input("Please set a score limit for this game:"))
    while game_on:

        background = pygame.transform.scale(pygame.image.load("image_files/board_persp_05.png").convert(), (CHESS_BOARD[0] * SCALAR, CHESS_BOARD[1] * SCALAR))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in ['w', 'a', 's', 'd'] and len(input_combo_black) < 2:
                    input_combo_black.append(key)
                    print(f"Black player key pressed: {key}, input_combo_black: {input_combo_black}")
                elif key in ['up', 'left', 'down', 'right'] and len(input_combo_white) < 2:
                    input_combo_white.append(key)
                    print(f"White player key pressed: {key}, input_combo_white: {input_combo_white}")

                 # Check for black player movement
                if len(input_combo_black) == 2:
                    dx_black, dy_black = 0, 0
                    if input_combo_black == ['w', 'a']:
                        dx_black, dy_black = -1, -2
                    elif input_combo_black == ['w', 'd']:
                        dx_black, dy_black = 1, -2
                    elif input_combo_black == ['s', 'a']:
                        dx_black, dy_black = -1, 2
                    elif input_combo_black == ['s', 'd']:
                        dx_black, dy_black = 1, 2
                    elif input_combo_black == ['a', 'w']:
                        dx_black, dy_black = -2, -1
                    elif input_combo_black == ['a', 's']:
                        dx_black, dy_black = -2, 1
                    elif input_combo_black == ['d', 'w']:
                        dx_black, dy_black = 2, -1
                    elif input_combo_black == ['d', 's']:
                        dx_black, dy_black = 2, 1

                    new_x_black, new_y_black = player_black.simulate_move(dx_black, dy_black)
                    #Player collision
                    if new_x_black == player_white.x and new_y_black == player_white.y:
                        
                        if player_black.holding_flag:
                            player_black.holding_flag = False
                            print(f"Black player dropped the flag!")
                            add_object(WHITE_FLAG, grid, Flag,  random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            flag_white = all_grid_objects[-1]
                            draw_grid(screen, grid)
                            pygame.display.update()
                        if player_white.holding_flag:
                            player_white.holding_flag = False
                            print(f"White player dropped the flag!")
                            add_object(BLACK_FLAG, grid, Flag,  random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            flag_black = all_grid_objects[-1]
                            draw_grid(screen, grid)
                            pygame.display.update()
                        else:
                            player_black.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            player_white.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2)) 
                    # Flag captured
                    elif new_x_black == flag_white.x and new_y_black == flag_white.y:
                        remove_object(grid, flag_white.x, flag_white.y)
                        player_black.move(dx_black, dy_black)
                        player_black.capture_flag()
                        print(f"Black has captured the flag!")
                    # Player scored
                    elif new_x_black == goal_black.x and new_y_black == goal_black.y:
                        if player_black.holding_flag:
                            player_black.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            flag_white = add_object(WHITE_FLAG, grid, Flag,  random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            player_black.add_points(1)
                        else:
                            player_black.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            print("No puppy guarding!")
                    # Move the player to unoccupied space
                    else:
                        player_black.move(dx_black, dy_black)
                    input_combo_black.clear()

                # Check for white player movement
                if len(input_combo_white) == 2:
                    dx_white, dy_white = 0, 0
                    if input_combo_white == ['up', 'left']:
                        dx_white, dy_white = -1, -2
                    elif input_combo_white == ['up', 'right']:
                        dx_white, dy_white = 1, -2
                    elif input_combo_white == ['down', 'left']:
                        dx_white, dy_white = -1, 2
                    elif input_combo_white == ['down', 'right']:
                        dx_white, dy_white = 1, 2
                    elif input_combo_white == ['left', 'up']:
                        dx_white, dy_white = -2, -1
                    elif input_combo_white == ['left', 'down']:
                        dx_white, dy_white = -2, 1
                    elif input_combo_white == ['right', 'up']:
                        dx_white, dy_white = 2, -1
                    elif input_combo_white == ['right', 'down']:
                        dx_white, dy_white = 2, 1

                    new_x_white, new_y_white = player_white.simulate_move(dx_white, dy_white)

                    # Player collision
                    if new_x_white == player_black.x and new_y_white == player_black.y:
                        
                        if player_white.holding_flag:
                            player_white.holding_flag = False
                            print(f"White player dropped the flag!")
                            player_white.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            player_black.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            flag_black = add_object(BLACK_FLAG, grid, Flag,  random.randint(1, ROWS - 2), random.randint(1, COLS - 2))

                        if player_black.holding_flag:
                            player_black.holding_flag = False
                            print(f"Black player dropped the flag!")
                            player_white.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            player_black.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            flag_black = add_object(WHITE_FLAG, grid, Flag,  random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                        else:
                            player_black.bounce(random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            player_white.bounce(random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                    # Black Flag captured by White
                    elif new_x_white == flag_black.x and new_y_white == flag_black.y:
                        player_white.capture_flag()
                        remove_object(grid, flag_black.x, flag_black.y)
                        player_white.move(dx_white, dy_white)
                        print(f"White has captured the flag!")
                    # Player scored
                    elif new_x_white == goal_white.x and new_y_white == goal_white.y:
                        if player_white.holding_flag:
                            player_white.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            flag_black = add_object(BLACK_FLAG, grid, Flag,  random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            player_white.add_points(1)
                        else:
                            player_white.bounce( random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
                            print("No puppy guarding!")
                    # Move the player to unoccupied space
                    else:
                        player_white.move(dx_white, dy_white)
                    input_combo_white.clear()
        if player_white.points_count == SCORE_LIMIT or player_black.points_count == SCORE_LIMIT:
            game_on = False


        screen.blit(background, (0, 0))
        # left_border = pygame.draw.line(screen, 'red', (30, 100), (30, 620), 1)
        # right_border = pygame.draw.line(screen, 'red', (725, 100), (725, 620), 1)
        # top_border = pygame.draw.line(screen, 'red', (30, 100), (725, 100), 1)
        # bottom_border = pygame.draw.line(screen, 'red', (30, 620), (725, 620), 1)
        
        # Draw the grid after handling events
        draw_grid(screen, grid)
        
        pygame.display.update()
        clock.tick(FPS)
    return player_black.points_count, player_white.points_count

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Horse of Course")
    clock = pygame.time.Clock()
    # Set up the grid
    grid = Grid(ROWS, COLS)
    # Create the players
    add_object(BLACK, grid, Player, ROWS - 1, random.randint(0, COLS - 2))
    add_object(WHITE, grid, Player, 0, random.randint(1, COLS - 1))
    add_object(BLACK_FLAG, grid, Flag, random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
    add_object(WHITE_FLAG, grid, Flag, random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
    add_object(BLACK_GOAL, grid, Goal, ROWS - 1, COLS - 1)
    add_object(WHITE_GOAL, grid, Goal, 0, 0)
    print(grid)
    black, white = main_loop(grid, screen, clock)

    if black > white:
        print(f"CONGRATULATIONS BLACK!, you scored {black}!")
        print(f"Better luck next time WHITE, you scored {white}")
    else:
        print(f"CONGRATULATIONS WHITE!, you scored {white}!")
        print(f"Better luck next time BLACK, you scored {black}")


if __name__ == "__main__":
    main()