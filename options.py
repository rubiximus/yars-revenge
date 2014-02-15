

#screen constants
window_size = (width, height) = (800, 600)
max_framerate = 60
black = (0, 0, 0)
white = (255, 255, 255)

#font options
font_size = 15

#player options
player_filename = "graphics/test_arrow4_alpha.png"
player_height = 30
player_width = 30
player_animation_delay = 10
player_speed = 5
player_args = (player_filename, player_height, player_width, player_animation_delay, player_speed)

#enemy base
mover_filename = "graphics/mover_base.png"
mover_top = 150
mover_bottom = 450
mover_speed = 2
mover_args = (mover_filename, mover_top, mover_bottom, mover_speed)

spinner_filename = "graphics/test_arrow2.png"
spinner_height = 30
spinner_width = 30
spinner_animation_delay = 5
spinner_first_time = 29
spinner_second_time = 30
spinner_args = (spinner_filename, spinner_height, spinner_width, spinner_animation_delay,
                spinner_first_time, spinner_second_time)
                
shooter_filename = "graphics/test_arrow2.png"
shooter_height = 30
shooter_width = 30
shooter_animation_delay = 3
shooter_speed = 2
shooter_wait_time = 30
shooter_args = (shooter_filename, shooter_height, shooter_width, shooter_animation_delay,
                shooter_wait_time)
                
#enemy shield
shield_filename = "graphics/cell2.png"

#the number of pixels the player is pushed left when colliding with a shield cell
cell_bounceback = 15
frames_to_eat_cell = 15

#homing bullet
homer_filename = "graphics/bullet.png"
homer_speed = 2

#player bullet
max_player_bullets = 1

bullet_filename = "graphics/bullet2.png"
bullet_speed = 8

#player cannon
deactivated_cannon_args = ()

standby_cannon_filename = "graphics/cell.png"
standby_cannon_args = (standby_cannon_filename, )

firing_cannon_filename = "graphics/cell.png"
firing_cannon_speed = 9
firing_cannon_args = (firing_cannon_filename, firing_cannon_speed)
