

import pygame
from pygame import Surface, mask

def split_frames(filename, height, width, single_row=False):
    """Splits a multi-sprite file into subsurfaces.
    filename is the image file containing the sprites
    height, width are the dimensions of the sprites
    
    returns a 2D list of Surfaces indexed [row][col]
    returns normal list when image file is one row and single_row is set to True
    
    TODO: return matching list of Masks
    """
    
    parent = pygame.image.load(filename).convert_alpha()
    parent_width, parent_height = parent.get_size()
    parent_rows = int(parent.get_height() / height)
    parent_cols = int(parent.get_width() / width)
    
    if parent_rows == 1 and single_row:
        return split_row(parent, parent_cols, 0, height, width)
    
    images = []
    masks = []
    
    for row in range(parent_rows):
        current_images, current_masks = split_row(parent, parent_cols, row, height, width)
        images.append(current_images)
        masks.append(current_masks)
        
    return images, masks
    
    
def split_row(parent, parent_cols, row, height, width):
    """split_frame helper function
    splits a single row of source surface
    """
    
    images = []
    masks = []
    
    for col in range(parent_cols):
        current_image = parent.subsurface((col*width, row*height, width, height))
        images.append(current_image)
        masks.append(mask.from_surface(current_image))
        
    return images, masks
