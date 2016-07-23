"""

options.py

Contains global game constants and base arguments for initializing sprites
These options should mostly be accessed by the main loop, levels, and level manager;
try to minimize access by other files like Sprite classes.

"""

#constants used in game initialization and levels

#screen constants
window_size = (width, height) = (800, 600)
max_framerate = 60
black = (0, 0, 0)
white = (255, 255, 255)

#font options
font_size = 15

#score and lives
initial_lives = 4
score_cell_shoot = 69
score_cell_eat = 169
score_mover_destroy = 1000
score_spinner_destroy = 2000
score_shooter_destroy = 6000

#player energy constants -- the energy given by eating a cell,
#touching enemy base, or catching a returning cannon shot;
#and the cost of activating the cannon
energy_from_cell = 1
energy_from_enemy = 2
energy_from_cannon = 4
cannon_energy_cost = 5
max_energy = 255

#the number of pixels the player is pushed left when colliding with a shield cell
cell_bounceback = 15
frames_to_eat_cell = 15

#maximum number of player bullets on the screen
max_player_bullets = 1

#death animation constants
death_animation_delay = 4
death_animation_total_runtime = 64

#win animation constants
win_animation_total_runtime = 120

#constructor arguments for sprites

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
mover_avg_transition = 10
mover_args = (mover_filename, mover_speed, mover_top, mover_bottom, mover_avg_transition)

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

#homing bullet
homer_filename = "graphics/bullet.png"
homer_speed = 1

#player bullet
bullet_filename = "graphics/bullet2.png"
bullet_speed = 8

#player cannon
deactivated_cannon_args = ()

standby_cannon_filename = "graphics/cell.png"
standby_cannon_args = (standby_cannon_filename, )

firing_cannon_filename = "graphics/cell.png"
firing_cannon_speed = 9
firing_cannon_args = (firing_cannon_filename, firing_cannon_speed)

#ion field
ion_top = 0
ion_bot = height
ion_left = 250
ion_right = 400
ion_delay = 6
ion_noise_width = 15
ion_noise_height = 2
ion_field_args = (ion_top, ion_bot, ion_left, ion_right, ion_noise_width, ion_noise_height, ion_delay)
