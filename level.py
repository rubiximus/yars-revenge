"""

level.py

Contains the Level class, which is the state for one game level

"""

import math

import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, collide_mask, spritecollide, groupcollide

from gamestate import GameState

from options import *
from vector import *
from ship import Ship, Bullet
from enemy_base import EnemyBase
from formations import formation, formation_center
from enemy_shield import EnemyShield
from homing_bullet import HomingBullet
from cannon import Cannon

class Level(GameState):
    """Level is a GameState with behavior for one full game level.

    Contains Sprites player, enemy, shield, hbullet, cannon, and Group player_bullets
    """
    
    def __init__(self, manager):
        """manager is required to be a child of GameManager with these functions:
        -kill_player()
        -end_level()
        """

        GameState.__init__(self, manager)

        self.player = Ship(*player_args)
        self.enemy = EnemyBase(mover_args, spinner_args, shooter_args, self.player)
        self.shield = EnemyShield(self.enemy, shield_filename, formation, formation_center)
        self.hbullet = HomingBullet(homer_filename, self.player, homer_speed)
        self.cannon = Cannon(deactivated_cannon_args, standby_cannon_args,
                             firing_cannon_args, self.player)
        self.player_bullets = Group()

        self.reset_positions()
        

    def update(self):
        self.player.update()
        self.enemy.update()
        self.shield.update()
        self.hbullet.update()
        self.cannon.update()
        self.player_bullets.update()
        
        self.collisions()


    def handle_events(self, events, keys):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    return False
                elif (e.key == K_z or
                      e.key == K_SPACE):
                    self.shoot()

        if keys[K_UP] and keys[K_RIGHT]:
            self.player.move(NORTHEAST)
        elif keys[K_UP] and keys[K_LEFT]:
            self.player.move(NORTHWEST)
        elif keys[K_DOWN] and keys[K_RIGHT]:
            self.player.move(SOUTHEAST)
        elif keys[K_DOWN] and keys[K_LEFT]:
            self.player.move(SOUTHWEST)
        elif keys[K_LEFT]:
            self.player.move(WEST)
        elif keys[K_RIGHT]:
            self.player.move(EAST)
        elif keys[K_UP]:
            self.player.move(NORTH)
        elif keys[K_DOWN]:
            self.player.move(SOUTH)

        return True
    

    def draw(self, screen):
        self.enemy.draw(screen)
        self.shield.draw(screen)
        self.player.draw(screen)
        self.hbullet.draw(screen)
        self.cannon.draw(screen)
        self.player_bullets.draw(screen)


    def collisions(self):
        """Handles collisions
        """

        player = self.player
        enemy = self.enemy
        shield = self.shield
        hbullet = self.hbullet
        cannon = self.cannon
        player_bullets = self.player_bullets
        
        #player with homing bullet
        if collide_mask(player, hbullet):
            self.kill_player()
        
        #player with enemy base
        if collide_mask(player, enemy):
            #if base in moving phase, give player energy
            if enemy.get_state_number() == EnemyBase.MOVING:
                self.player.give_energy(energy_from_enemy)
            #if base in spinning or shooting phase, kill player
            elif enemy.get_state_number() == EnemyBase.SPINNING:
                self.kill_player()
            elif enemy.get_state_number() == EnemyBase.SHOOTING:
                self.kill_player()
                
        #player with cell
        #-hitting a cell will bounce the player a bit to the left
        #-if the player hit the cell twice in a short enough span,
        # the cell is eaten and the player gets energy
        #-in case of multiple collisions, deal with cell closest to player's center
        #
        #TODO: This still isn't quite right.
        #Should be able to eat top/bottom rows with diagonal movement.
        #(vertical movement should still move player all the way left)
        pc_collides = spritecollide(player, shield, False, collide_mask)
        center_cell = self.find_centermost_cell(pc_collides)
        if center_cell is not None:
            player.rect.right = center_cell.rect.left - cell_bounceback
            
            if not center_cell.marked:
                center_cell.mark()
            elif shield.can_eat():
                player.give_energy(energy_from_cell)
                center_cell.kill()
                self.manager.add_score(score_cell_eat)
                shield.start_delay(frames_to_eat_cell)
            
        #player with cannon
        if collide_mask(player, cannon):
            #if in deactivated phase, try spending required energy to activate
            if (cannon.get_state_number() == Cannon.DEACTIVATED and 
                player.spend_energy(cannon_energy_cost)):
                cannon.start_standby()
            #if in firing phase, kill player
            if cannon.get_state_number() == Cannon.FIRING:
                self.kill_player()
            #if in returning phase, give energy and deactivate cannon
            if cannon.get_state_number() == Cannon.RETURNING:
                cannon.start_transition(Cannon.DEACTIVATED)
                player.give_energy(energy_from_cannon)
                
        #cannon with cell
        #kill one cell and reverse cannon direction
        #assuming this is only possible if cannon in firing state
        if cannon.get_state_number() == Cannon.FIRING:
            cannon_collides = spritecollide(cannon, shield, False, collide_mask)
            if len(cannon_collides) > 0:
                cannon_collides[0].kill()
                self.manager.add_score(score_cell_shoot)
                cannon.start_transition(Cannon.RETURNING)
            
        #cannon with enemy base -- only if cannon in firing state
        #give points corresponding to enemy state and end level
        #if enemy base is in shooting state, player also gets a life
        if cannon.get_state_number() == Cannon.FIRING and collide_mask(cannon, enemy):
            if enemy.get_state_number() == EnemyBase.MOVING:
                self.manager.add_score(score_mover_destroy)
            elif enemy.get_state_number() == EnemyBase.SPINNING:
                self.manager.add_score(score_spinner_destroy)
            elif enemy.get_state_number() == EnemyBase.SHOOTING:
                self.manager.add_score(score_shooter_destroy)
                self.manager.give_life()
            self.end_level()
        
        #player's bullet with cell
        #kill player bullet but remove cells in a cross pattern
        #if somehow one bullet hits multiple cells one is arbitrarily selected
        bc_collides = groupcollide(player_bullets, shield, True, False, collide_mask)
        for current_bullet in bc_collides.keys():
            self.manager.add_score(score_cell_shoot)
            shield.remove_cross(bc_collides[current_bullet][0])


    def find_centermost_cell(self, cells):
        """Given a list of Cell sprites, 
        returns the one whose rect.centery is closest to the player's rect.centery
        
        Returns None if list is empty
        """
        
        closest_cell = None
        
        for current_cell in cells:
            current_dist = abs(current_cell.rect.centery - self.player.rect.centery)
            if closest_cell is None or current_dist < closest_dist:
                closest_cell = current_cell
                closest_dist = current_dist

        return closest_cell


    def shoot(self):
        """If cannon can be fired, fires cannon.
        
        Otherwise creates bullet moving from player's center along player's direction
        as long as options.max_player_bullets won't be exeeded
        """
        
        if self.cannon.start_transition(Cannon.FIRING):
            return        
        
        if len(self.player_bullets) < max_player_bullets:
            new_bullet = Bullet(bullet_filename, bullet_speed, 
                                self.player.get_rect().center, self.player.get_direction())
            self.player_bullets.add(new_bullet)


    def reset_positions(self):
        """Moves sprites to their initial locations:
        player starts in left center facing south and with 0 energy
        enemy bullet starts on enemy base
        enemy base is in moving state
        cannon is in deactivated state
        """

        self.player.rect.midleft = (10, int(height/2))
        self.player.set_direction(SOUTH)
        self.player.reset_energy()
        self.enemy.resume_mover_state()
        self.cannon.start_deactivated()
        self.hbullet.rect.center = self.enemy.rect.center




    def kill_player(self):
        print("You died.")

        self.manager.kill_player()
        self.reset_positions()

        self.player 


    def end_level(self):
        print("You won the level!")
        
        self.manager.next_level()
