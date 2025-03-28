import pygame

#Player settings
PLAYER_START_X = 100
PLAYER_START_Y = 200
PLAYER_SIZE = 0.8

class Player(pygame.sprite.Sprite):
    points_count = 0
    holding_flag = False
    def __init__(self,color,grid,x,y):
        super().__init__()
        self.grid = grid
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(color).convert_alpha(), (int(PLAYER_SIZE * 100), int(PLAYER_SIZE * 100)))
        if color == "image_files\B_Knight1.png":
            self.color = "BLACK"
        elif color == "image_files\W_Knight1.png":
            self.color = "WHITE"
    
    def __str__(self):
        return f"({self.color}, {self.__class__.__name__})"
    
    def __repr__(self):
        return f"({self.color},{self.__class__.__name__},{self.x},{self.y})"

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within the grid bounds
        if 0 <= new_x < self.grid.width and 0 <= new_y < self.grid.height:
            # Check if the new position is empty
            if self.grid.get(new_x, new_y) is None:
                # Update the grid
                self.grid.set(self.x, self.y, None)
                self.grid.set(new_x, new_y, self)
                
                # Update the player's position
                self.x = new_x
                self.y = new_y
                print(f"Moved to ({self.x}, {self.y})")
            else:
                print(f"Position ({new_x}, {new_y}) is occupied")
        else:
            print(f"Position ({new_x}, {new_y}) is out of bounds")

    def bounce(self, dx, dy):
        # Bounce the player back to a new position
        self.grid.set(self.x, self.y, None)
        self.x = dx
        self.y = dy
        self.grid.set(self.x, self.y, self)
        self.holding_flag = False
        print(f"{self.color} Bounced to ({self.x}, {self.y})")

    # Checks where the player would move if they were to move in the direction of dx, dy
    # This is useful for determining collisions, picking up flags, or scoring.
    def simulate_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        return new_x, new_y
    # Increments the player's score by points
    def add_points(self, points):
        self.points_count += points
        print(f"{self.color} Player points: {self.points_count}")

    def capture_flag(self):
        self.holding_flag = True
        print(f"{self.color} Player captured the flag!")

class Flag(pygame.sprite.Sprite):
    def __init__(self, color, grid, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(color).convert_alpha(), (int(PLAYER_SIZE * 100), int(PLAYER_SIZE * 100)))
        self.grid = grid
        self.x = x
        self.y = y
        if color == "image_files\B_Pawn1.png":
            self.color = "BLACK_FLAG"
        elif color == "image_files\W_Pawn1.png":
            self.color = "WHITE_FLAG"

    def bounce(self, dx, dy):
        # Bounce the player back to a new position
        self.grid.set(self.x, self.y, None)
        self.x = dx
        self.y = dy
        self.grid.set(self.x, self.y, self)
        print(f"Bounced to ({self.x}, {self.y})")
    
    def __str__(self):
        return f"({self.color}, {self.__class__.__name__})"
    
    def __repr__(self):
        return f"({self.color}, {self.__class__.__name__}, {self.x}, {self.y})"

class Goal(pygame.sprite.Sprite):
    def __init__(self, color, grid, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(color).convert_alpha(), (int(PLAYER_SIZE * 100), int(PLAYER_SIZE * 100)))
        self.grid = grid
        self.x = x
        self.y = y
        if color == "image_files\B_Queen.png":
            self.color = "BLACK_GOAL"
        elif color == "image_files\W_Queen.png":
            self.color = "WHITE_GOAL"
    def __str__(self):
        return f"({self.color}, {self.__class__.__name__})"
    
    def __repr__(self):
        return f"({self.color}, {self.__class__.__name__}, {self.x}, {self.y})"