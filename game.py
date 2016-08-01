"""

game.py

Global initializations and main loop for general game

"""

import sys
import math

import pygame
from pygame import key
from pygame import event
from pygame.time import Clock
from pygame.font import Font, get_default_font

import options as opt
from yarsmanager import YarsManager

def main():
    """Main program loop"""
    
    pygame.init()
    screen = pygame.display.set_mode(opt.window_size)
    
    sys_font = Font(get_default_font(), opt.font_size)
    clock = Clock()
    
    manager = YarsManager()

    running = True
    
    while running:
        #limit framerate and prepare FPS display text
        clock.tick(opt.max_framerate)
        fps = clock.get_fps()
        fps_text = sys_font.render("FPS: {0:.1f}".format(fps), False, opt.white)
        
        if event.get(pygame.QUIT):
            sys.exit()

        running = manager.handle_events(event.get(), key.get_pressed())
        manager.update()

        screen.fill(opt.black)
        manager.draw(screen)
        screen.blit(fps_text, fps_text.get_rect(top = 0, right = opt.width))
        pygame.display.update()
		
    sys.exit()


if __name__ == '__main__':
    main()
