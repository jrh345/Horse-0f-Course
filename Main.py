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

def get_score_limit(screen, clock):
    """
    Display an input box for the user to enter a score limit.
    """
    pygame.font.init()
    font = pygame.font.Font(None, 36)  # Create a font object
    input_text = ""  # Store the user's input
    input_active = True  # Flag to keep the input box active
    background = pygame.transform.scale(pygame.image.load(EPIC_BACKGROUND).convert(), (WIDTH, HEIGHT))
    #screen.blit(background, (0, 0))  # Display the background image

    while input_active:
        
        prompt_text = font.render("Enter Score Limit (Press Enter to Confirm):", True, (255, 255, 255))
        screen.blit(background, (0, 0))  # Display the background image
        screen.blit(prompt_text, (50, 100))  # Display the prompt text
        # Render the input text dynamically
        input_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(input_surface, (50, 150))  # Display the input text

        pygame.display.update()  # Refresh the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Confirm input with Enter
                    if input_text.isdigit():  # Validate that the input is a number
                        return int(input_text)
                    else:
                        input_text = ""  # Clear invalid input
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode  # Add the typed character to the input
        
        clock.tick(FPS)  # Limit the frame rate
def reset_game(grid,screen):
    rest_text = "Do you want to play again? (y/n)"
    font = pygame.font.Font(None, 36)  # Create a font object
    rest_text_surface = font.render(rest_text, True, (255, 255, 255))
    screen.blit(rest_text_surface, (WIDTH//4, HEIGHT//2))  # Display the prompt text
    pygame.display.update()  # Refresh the display
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'y':
                    for y in range(COLS):
                        for x in range(ROWS):
                            remove_object(grid, x, y)
                    return True
                elif key == 'n':
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                        goodbye_text = font.render("Thanks for playing!", True, (255, 255, 255))
                        screen.blit(goodbye_text, (WIDTH * 4/5 - 30, HEIGHT * 7/10))
                        pygame.display.update()
                    

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

    SCORE_LIMIT = get_score_limit(screen, clock)
    screen.fill((0, 0, 0))  # Clear the screen with a black background
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    start_time = pygame.time.get_ticks()
    while game_on:
        # Calculate elapsed time
        elapsed_time_ms = pygame.time.get_ticks() - start_time
        elapsed_time_sec = elapsed_time_ms // 1000
        minutes = elapsed_time_sec // 60
        seconds = elapsed_time_sec % 60
        timer_text = f"Time: {minutes:02}:{seconds:02}"

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
        
        # Draw the grid after handling events
        draw_grid(screen, grid)

        # Draw the players and their scores
        screen.blit(player_black.image, (BLACK_PLAYER_X, BLACK_PLAYER_Y))
        screen.blit(player_white.image, (WHITE_PLAYER_X, WHITE_PLAYER_Y))

        black_score_text = font.render(f"Black Score: {player_black.points_count}", True, (255, 255, 255))
        white_score_text = font.render(f"White Score: {player_white.points_count}", True, (255, 255, 255))

        # Draw the timer
        timer_text_surface = font.render(timer_text, True, (255, 255, 255))
        screen.fill((0, 0, 0), (WIDTH * 3/5 - 25, HEIGHT * 9/10, WIDTH * 3/5 + 25, HEIGHT * 9/10 + 20))
        screen.blit(timer_text_surface, (WIDTH * 3/5 - 25, HEIGHT * 9/10))

        # Clears the score text before drawing the new score
        screen.fill((0, 0, 0), (WHITE_SCORE_X, WHITE_SCORE_Y, WHITE_SCORE_X + 50, WHITE_SCORE_Y+ 20))
        screen.fill((0, 0, 0), (BLACK_SCORE_X, BLACK_SCORE_Y, BLACK_SCORE_X + 50, BLACK_SCORE_Y + 20))
        screen.blit(black_score_text, (BLACK_SCORE_X, BLACK_SCORE_Y))
        screen.blit(white_score_text, (WHITE_SCORE_X, WHITE_SCORE_Y))
        
        pygame.display.update()
        clock.tick(FPS)
    return player_black.points_count, player_white.points_count

def main():
    
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 36)  # Create a font object
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Horse of Course")
    clock = pygame.time.Clock()
    
    # Set up the grid
    grid = Grid(ROWS, COLS)
    go_again = True
    while go_again:
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
            black_victory_text = font.render(f"Black Wins!", True, (255, 255, 255))
            screen.blit(black_victory_text, (WIDTH * 4/5, HEIGHT * 6/10))
            pygame.display.update()
        else:
            white_victory_text = font.render(f"White Wins!", True, (255, 255, 255))
            screen.blit(white_victory_text, (WIDTH * 4/5, HEIGHT * 6/10))
            pygame.display.update()
        go_again = reset_game(grid,screen)


if __name__ == "__main__":
    main()