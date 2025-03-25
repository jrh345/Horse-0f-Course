class Grid:
    from copy import deepcopy
    """
    2D grid with (x, y) int indexed internal storage
    Has .width .height size properties
    """
    def __init__(self, width, height):
        """
        Create grid `array` width by height. Create a Grid object with
        a width, height, and array. Initially all locations hold None.
        >>> grid = Grid(2, 2)
        >>> grid.array
        [[None, None], [None, None]]
        """
        self.height = height
        self.width = width
        self.array = []
        for y in range(height):
            row = []
            for x in range (width):
                row.append(None)
            self.array.append(row)

    def in_bounds(self,x,y):
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return False
        else:
            return True
        
    def get(self, x, y):
        """
        Gets the value stored value at (x, y).
        (x, y) should be in bounds.
        >>> grid = Grid(2, 2)
        >>> grid.array = [[1, 2], [4, 5]]
        >>> grid.get(0, 1)
        4
        >>> grid.get(1, 0)
        2
        """
        if not self.in_bounds(x,y):
            raise IndexError
        return self.array[y][x]
    def set(self, x, y, val):
        """
        Sets a new value into the grid at (x, y).
        (x, y) should be in bounds.
        >>> grid = Grid(2, 2)
        >>> grid.set(1, 1, "Milk")
        >>> grid.set(1, 0, "Dud")
        >>> grid.array
        [[None, 'Dud'], [None, 'Milk']]
        """
        if self.in_bounds(x,y) == False:
            raise IndexError
        self.array[y][x] = val
    
    def __str__(self):
        return f"Grid({self.height}, {self.width}, first = {self.array[0][0]})"
    
    def __repr__(self):
        return f"Grid.build({self.array})"
    
    def __eq__(self, other):
        if isinstance(other, Grid):
            return self.array == other.array
        elif isinstance(other,list):
            return self.array == other
        else:
            return False
    @staticmethod
    def check_list_malformed(lst):
        """
        Given a list that represents a 2D nested Grid, check that it has the
        right shape. Raise a ValueError if it is malformed.
        >>> Grid.check_list_malformed([[1, 2], [4, 5]])
        >>> Grid.check_list_malformed(1)
        Traceback (most recent call last):
        ...
        ValueError: Input must be a non-empty list of lists.
        >>> Grid.check_list_malformed([[1, 2], [4, 5, 6]])
        Traceback (most recent call last):
        ...
        ValueError: All items in list must be lists of the same length.
        >>> Grid.check_list_malformed([[1, 2], 3])
        Traceback (most recent call last):
        ...
        ValueError: Input must be a list of lists.
        """
        if not isinstance(lst,list):
            raise ValueError
        if lst == []:
            raise ValueError
        if not all(isinstance(item,list) for item in lst):
            raise ValueError
        if not all(len(item) == len(lst[0]) for item in lst):
            raise ValueError

    @staticmethod
    def build(lst):
        """
        Given a list that represents a 2D nested Grid construct a Grid object.
        Grid.build([[1, 2, 3], [4, 5 6]])
        >>> Grid.build([[1, 2, 3], [4, 5, 6]]).array
        [[1, 2, 3], [4, 5, 6]]
        """
        Grid.check_list_malformed(lst)
        height = len(lst)
        width = len(lst[0])
        new_grid_object = Grid(width,height)

        for y in range(height):
            for x in range (width):
                new_grid_object.set(x,y,lst[y][x])
        return new_grid_object
    
    def copy(self):
        grid_copy = self.deepcopy()
        return grid_copy