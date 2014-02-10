

import sys
import math

import pygame
from pygame import key
from pygame import event
from pygame.locals import *
from pygame.time import Clock
from pygame.font import Font, get_default_font
from pygame.sprite import Sprite, Group, collide_mask, spritecollide, groupcollide

from options import *
from vector import *
from ship import Ship, Bullet
from enemy_base import EnemyBase
from formations import formation, formation_center
from enemy_shield import EnemyShield
from homing_bullet import HomingBullet
from cannon import Cannon

player_bullets = Group()

def handle_events():
    """Traverses events queue and executes behavior for relevant events.
    May be used for keypress actions that only activate on key down/up.

    returns True iff the QUIT event hasn't been triggered
    or the Esc key hasn't been pressed.
    """

    for e in event.get():
        if e.type == pygame.QUIT:
            return False
        
        elif e.type == pygame.KEYDOWN:
            if e.key == K_ESCAPE:
                return False
            elif e.key == K_z:
                shoot()
            elif e.key == K_1:
                enemy.start_transition(enemy.SPINNING)
            elif e.key == K_2:
                cannon.start_transition(cannon.STANDBY)
                
    return True


def keyboard():
    """Checks for relevent keypresses and performs the corresponding action.
	These are actions which activate any frame the key is down, e.g. moving.
	"""
    
    key_states = key.get_pressed()
        
    if key_states[K_UP] and key_states[K_RIGHT]:
        player.move(NORTHEAST)
    elif key_states[K_UP] and key_states[K_LEFT]:
        player.move(NORTHWEST)
    elif key_states[K_DOWN] and key_states[K_RIGHT]:
        player.move(SOUTHEAST)
    elif key_states[K_DOWN] and key_states[K_LEFT]:
        player.move(SOUTHWEST)
    elif key_states[K_LEFT]:
        player.move(WEST)
    elif key_states[K_RIGHT]:
        player.move(EAST)
    elif key_states[K_UP]:
        player.move(NORTH)
    elif key_states[K_DOWN]:
        player.move(SOUTH)


def collisions():
    """Handles collisions
    """
    
    #player with homing bullet
    if collide_mask(player, hbullet):
        kill_player()
    
    #player with enemy base
    if collide_mask(player, enemy):
        #TODO: if base in moving phase, give player energy
        if enemy.get_state_number() == enemy.MOVING:
            pass
        #if base in moving or shooting phase, kill player
        if enemy.get_state_number() == enemy.SPINNING:
            kill_player()
        if enemy.get_state_number() == enemy.SHOOTING:
            kill_player()
            
    #player with cell
    #either the cell is eaten or the player is moved left until the sprites don't collide
    #in case of multiple collisions, just deal with cell closest to player's center
    #
    #TODO: This still isn't quite right.
    #Should be able to eat top/bottom rows with vertical movement.
    pc_collides = spritecollide(player, shield, False, collide_mask)
    center_cell = find_centermost_cell(pc_collides)
    if center_cell is not None:
        player.rect.right = center_cell.rect.left - cell_bounceback
        
        if not center_cell.marked:
            center_cell.mark()
        elif shield.can_eat():
            center_cell.kill()
            shield.start_delay(frames_to_eat_cell)
        
    #player with cannon
    if collide_mask(player, cannon):
        #if in firing phase, kill player
        if cannon.get_state_number() == cannon.FIRING:
            kill_player()
        #TODO: if in returning phase, give energy
        if cannon.get_state_number() == cannon.RETURNING:
            pass
            
    #cannon with cell
    #kill one cell and reverse cannon direction
    #assuming this is only possible if cannon in firing state
    if cannon.get_state_number() == cannon.FIRING:
        cannon_collides = spritecollide(cannon, shield, False, collide_mask)
        if len(cannon_collides) > 0:
            cannon_collides[0].kill()
            cannon.start_transition(cannon.RETURNING)
        
    #cannon with enemy base
    #end level only if cannon in firing state
    if cannon.get_state_number() == cannon.FIRING and collide_mask(cannon, enemy):
        end_level()
    
    #player's bullet with cell
    #kill player bullet but remove cells in a cross pattern
    #if somehow one bullet hits multiple cells one is arbitrarily selected
    bc_collides = groupcollide(player_bullets, shield, True, False, collide_mask)
    for current_bullet in bc_collides.keys():
        shield.remove_cross(bc_collides[current_bullet][0])


def find_centermost_cell(cells):
    """Given a list of Cell sprites, 
    returns the one whose rect.centery is closest to the player's rect.centery
    
    Returns None if list is empty
    """
    
    closest_cell = None
    
    for current_cell in cells:
        current_dist = abs(current_cell.rect.centery - player.rect.centery)
        if closest_cell is None or current_dist < closest_dist:
            closest_cell = current_cell
            closest_dist = current_dist

    return closest_cell


def shoot():
    """If cannon can be fired, fires cannon.
    
    Otherwise creates bullet moving from player's center along player's direction
    as long as options.max_player_bullets won't be exeeded
    """
    
    if cannon.start_transition(cannon.FIRING):
        return        
    
    if len(player_bullets) < max_player_bullets:
        new_bullet = Bullet(bullet_filename, bullet_speed, 
                            player.get_rect().center, player.get_direction())
        player_bullets.add(new_bullet)


def kill_player():
    #print("Die, player!")
    pass


def end_level():
    #print("You win!")
    pass


def main():
    """Main program loop"""
    
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    
    sys_font = Font(get_default_font(), font_size)
    clock = Clock()
    
    global player, enemy, shield, hbullet, cannon
    player = Ship(*player_args)
    enemy = EnemyBase(mover_args, spinner_args, shooter_args, player)
    shield = EnemyShield(enemy, shield_filename, formation, formation_center)
    hbullet = HomingBullet(homer_filename, player, homer_speed)
    cannon = Cannon(deactivated_cannon_args, standby_cannon_args, firing_cannon_args, player)
	
    running = True
    
    while running:
        #limit framerate and prepare FPS display text
        clock.tick(max_framerate)
        fps = clock.get_fps()
        fps_text = sys_font.render("FPS: {0:.1f}".format(fps), False, white)
        
        keyboard()
        running = handle_events()
        
        player.update()
        enemy.update()
        shield.update()
        hbullet.update()
        cannon.update()
        player_bullets.update()
        
        collisions()
        
        screen.fill(black)
        screen.blit(fps_text, fps_text.get_rect(top = 0, right = width))
        enemy.draw(screen)
        shield.draw(screen)
        player.draw(screen)
        hbullet.draw(screen)
        cannon.draw(screen)
        player_bullets.draw(screen)
        pygame.display.update()
		
    sys.exit()


if __name__ == '__main__':
    main()