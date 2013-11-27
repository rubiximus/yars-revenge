"""
shield.py

A shield is a sprite group representing the shield around an enemy base.
This version will be a basic shield where the cells maintain positions relative
to the target's rectangle following a given formation. (see formations.py)

EnemyShield expects the target object to provide two functions:
get_rect() which returns the target's rectangle
is_followable() which returns True if the target wants to be followed

"""

import pygame
from pygame.sprite import Sprite, Group

class EnemyShield(Group):
    """Things an EnemyShield will need:
    -a target to follow; expected to have a get_rect() function
    -cell sprite filename
    -a formation
    -a position (row, col) in the formation corresponding to the UPPER LEFT of the target
    """
    
    def __init__(self, target, sprite_filename, formation, target_position):
    
        Group.__init__(self)
        
        self.target = target
        self.sprite_filename = sprite_filename
        self.target_position = target_position
        
        #this image is passed to each Cell object
        cell_image = pygame.image.load(sprite_filename).convert_alpha()
        
        #convert formation list into table of cell sprites
        #offsets are the difference between current cell and target cell
        #since first cell is (0, 0) these start as negative of the target
        row_offset = -target_position[0]
        cells = []
        for row in formation:
            col_offset = -target_position[1]
            cells_row = []
            for col in row:
                #0 means the cell is empty
                if col == 0:
                    cells_row.append(None)
                #1 means a cell sprite should be added here
                elif col == 1:
                    new_cell = Cell(row_offset, col_offset, cell_image, target)
                    Group.add(self, new_cell)
                    cells_row.append(new_cell)
                #anything else means wtf are you doing
                else: raise
                col_offset += 1
            cells.append(cells_row)
            row_offset += 1
            
        self.cells = cells
        
        self.delay = 0
    
    
    def update(self):
        """Updates cells' positions only if target is followable"""
        
        if self.target.is_followable():
            Group.update(self)
            
        if self.delay > 0:
            self.delay -= 1
            
            
    def remove(self, *sprites):
        
        for current_sprite in sprites:
            if current_sprite not in self: continue
            
            row, col = self.get_cell_row_col(current_sprite)
            self.cells[row][col] = None
            
        Group.remove(self, *sprites)
            
            
    def remove_cross(self, cell):
        """Kills the given cell as well as the cells E, NE, SE, and twice E of it.
        
        i.e. the given cell is the left arm of a plus sign of cells removed
        """
        
        row, col = self.get_cell_row_col(cell)
        
        max_row = len(self.cells) - 1
        max_col = len(self.cells[0]) - 1
        
        #if else blocks to prevent indexing errors
        if col == max_col:
            ne_cell = None
            e_cell = None
            se_cell = None
            ee_cell = None
            
        else:
            e_cell = self.cells[row][col + 1]
        
            if row == 0:
                ne_cell = None
            else:
                ne_cell = self.cells[row - 1][col + 1]
                
            if row == max_row:
                se_cell = None
            else:
                se_cell = self.cells[row + 1][col + 1]
                
            if col + 1 == max_col:
                ee_cell = None
            else:
                ee_cell = self.cells[row][col + 2]
        
        self.remove(cell, ne_cell, e_cell, se_cell, ee_cell)
        
        
    def get_cell_row_col(self, cell):
        """Returns the (row, col) tuple for the given cell's location in the
        EnemyShield.cells array
        """
        
        row = cell.row_offset + self.target_position[0]
        col = cell.col_offset + self.target_position[1]
        
        return (row, col)
        
        
    def can_eat(self):
        return self.delay == 0
        
    def start_delay(self, delay_amount):
        self.delay = delay_amount
        

class Cell(Sprite):
    """Dummy sprite that maintains relative position to the center position
    and contains proper function overrides for behavior of being killed
    """
    
    def __init__(self, row_offset, col_offset, cell_image, target):
        """Set attributes and update to position"""
        
        Sprite.__init__(self)
        
        self.image = cell_image
        self.row_offset = row_offset
        self.col_offset = col_offset
        self.target = target
        
        self.marked = False
        
        self.update()


    def update(self):
        """Move cell to maintain relative position to target"""
    
        height = self.image.get_height()
        width = self.image.get_width()
        target_left, target_top = self.target.get_rect().topleft
        cell_top = target_top + self.row_offset * height
        cell_left = target_left + self.col_offset * width
        self.rect = self.image.get_rect(topleft = (cell_left, cell_top))
        
        if self.marked:
            if self.tick >= 10:
                self.marked = False
            else: self.tick += 1
        
        
    def mark(self):
        """Marks the cell. A marked cell can be eaten by the player"""
        
        self.marked = True
        self.tick = 0
