#game setup
WIDTH = 1080
HEIGHT = 750
FPS = 60
CHESS_BOARD = [236,236]
TOP_BORDER = [(60,60), (700,60)]
SCALAR = 3.2

#Player settings
PLAYER_START_X = 100
PLAYER_START_Y = 200
PLAYER_SIZE = 0.15
PLAYER_SPEED = 8

#PLayer Icons and scoreboard
#White Player coordinates
WHITE_PLAYER_X = WIDTH * 4/5
WHITE_PLAYER_Y = HEIGHT * 1/10
#White Player scoreboard
WHITE_SCORE_X = WIDTH * 4/5
WHITE_SCORE_Y = HEIGHT * 2/10

#Black Player coordinates
BLACK_PLAYER_X = WIDTH * 4/5
BLACK_PLAYER_Y = HEIGHT * 4/10

#Black Player scoreboard
BLACK_SCORE_X = WIDTH * 4/5
BLACK_SCORE_Y = HEIGHT * 5/10

#Player Colors
#BLACK and WHITE are the images for the knight pieces

BLACK = "image_files\B_Knight1.png"
BLACK_FLAG = "image_files\B_Pawn1.png"
BLACK_GOAL = "image_files\B_Queen.png"
WHITE = "image_files\W_Knight1.png"
WHITE_FLAG = "image_files\W_Pawn1.png"
WHITE_GOAL = "image_files\W_Queen.png"

#CUSTOM GRID SETTINGS
HORIZONTAL_SPACING = 85
VERTICAL_SPACING = 64
GRID_OFFSET_X = 37
GRID_OFFSET_Y = 85
ROWS,COLS = 8,8
