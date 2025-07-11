import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(100, screen.get_height() / 2)
enemy_pos = pygame.Vector2(screen.get_width() - 100 , screen.get_height() / 2)
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# ball
last_ball_x = 0
ball_vX = 0
ball_radius = 30

ball_start_dir = random.choice([True, False])
if ball_start_dir == True :
    ball_vX = 500
else:
    ball_vX = -500

# player
player_vX = 0
paddle_width = 20
max_hp = 100
player_hp = max_hp
player_damage = 0
inv_time = 0.2
last_damaged = 0
current_time = 0


# enemy
enemy_hp = max_hp 
enemy_damage = 0
detection_radius = 100
reaction_time = 0.3
enemy_vX = 0
enemy_last_damaged = 0


# hp system
#------------------------------------
base_damage = 0
speed_damage_mult = 0.003

def calculate_damage(ball_speed, paddle_speed):
    speed_damage = abs(ball_speed - paddle_speed) * speed_damage_mult
    
    total_damage = base_damage + speed_damage
    return round(total_damage)
    
def draw_hp_bar(surface, x, y, current_hp, max_hp, color, width = 200, height = 20):
    pygame.draw.rect(surface, "darkgray", (x, y, width, height))
    
    hp_percentage = current_hp / max_hp
    hp_width = int(width * hp_percentage)
    
    if hp_percentage > 0.6:
        bar_color = "green"
    elif hp_percentage > 0.3:
        bar_color = "yellow"
    else:
        bar_color = "red"
        
    if hp_width > 0:
        pygame.draw.rect(surface, bar_color, (x, y, hp_width, height))
        
def draw_player_inv():
    current_time = pygame.time.get_ticks() / 1000
    is_inv = current_time - last_damaged_time < inv_duration
    
    if is_inv:
        if int(current_time * 10) % 2:
            color = "lightblue"
        else:
            color = "blue"
    else:
        color = "blue"

    pygame.draw.line(screen, color, (player_pos.x, player_pos.y + 40), (player_pos.x, player_pos.y - 40), paddle_width)
    
#------------------------------------

# start
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill("black")
    
    dt = clock.tick(60) / 1000
        
#render game here
#-------------------------------------------------------
    
    #ball logic
    #---------------------------
    
    pygame.draw.circle(screen, "white", ball_pos, ball_radius)
    
    last_ball = ball_pos.x - ball_vX * dt
    ball_pos.x += ball_vX * dt

    if ball_pos.x >= 1280 - ball_radius and ball_vX > 0:
        ball_vX *= -1
    
    if ball_pos.x <= 0 + ball_radius and ball_vX < 0:
        ball_vX *= -1
             
    # player colision check
    
    current_time = pygame.time.get_ticks() / 1000
    
    player_left = player_pos.x - paddle_width / 2
    player_right = player_pos.x + paddle_width / 2
    
    
    if (player_left - ball_radius <= ball_pos.x <= player_right + ball_radius):
        if ball_vX < 0 and last_ball > player_right:
            if current_time - last_damaged >= inv_time:
                player_damage = calculate_damage(ball_vX, player_vX)
                player_hp = max(0, player_hp - player_damage)
                last_damaged = current_time
                
            ball_vX = abs(ball_vX) + player_vX * 0.75
            ball_pos.x = player_right + ball_radius
        elif ball_vX > 0 and last_ball < player_left:
            if current_time - last_damaged >= inv_time:
                player_damage = calculate_damage(ball_vX, player_vX)
                player_hp = max(0, player_hp - player_damage)
                last_damaged = current_time
            
            ball_vX = -abs(ball_vX) + player_vX * 0.75
            ball_pos.x = player_left - ball_radius 

    # enemy colision check
    
    enemy_left = enemy_pos.x - paddle_width / 2
    enemy_right = enemy_pos.x + paddle_width / 2
     
    if (enemy_left - ball_radius <= ball_pos.x <= enemy_right + ball_radius):
        if ball_vX < 0 and last_ball > enemy_right:
            if current_time - enemy_last_damaged >= inv_time:
                enemy_damage = calculate_damage(ball_vX, player_vX)
                enemy_hp = max(0, enemy_hp - enemy_damage)
                enemy_last_damaged = current_time
                
            ball_vX = abs(ball_vX) + enemy_vX * 0.75
            ball_pos.x = enemy_right + ball_radius
        elif ball_vX > 0 and last_ball < enemy_left:
            if current_time - enemy_last_damaged >= inv_time:
                enemy_damage = calculate_damage(ball_vX, player_vX)
                enemy_hp = max(0, enemy_hp - enemy_damage)
                enemy_last_damaged = current_time
                
            ball_vX = -abs(ball_vX) + enemy_vX * 0.75
            ball_pos.x = enemy_left - ball_radius 

    ball_vX = (max(min(ball_vX, 1000), -1000))
    ball_vX *= 1.01
    
    #---------------------------
    
    # player logic
    #---------------------------
    
    pygame.draw.line(screen, "blue", (player_pos.x, player_pos.y + 40), (player_pos.x, player_pos.y - 40), paddle_width)
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_vX -= 30
          
    if keys[pygame.K_d]:
        player_vX += 30
        
    player_pos.x += player_vX * dt
    
    if player_vX > 0:
        player_vX -= 3
    elif player_vX < 0:
        player_vX += 3 
    
    if player_pos.x >= 1280 :
        player_vX = -60
        player_pos.x = 1279
        
    if player_pos.x <= 0:
        player_vX = 60
        player_pos.x = 1
    #---------------------------
    
    # enemy logic
    #---------------------------
    pygame.draw.line(screen, "red", (enemy_pos.x, enemy_pos.y + 40), (enemy_pos.x, enemy_pos.y - 40), paddle_width)
    
    enemy_ball_distance = abs(ball_pos.x - enemy_pos.x)
    enemy_ball_time = enemy_ball_distance / ball_vX
    
    if enemy_ball_time < reaction_time :
        if enemy_ball_time <= 0 :
            pass
        else :
            if enemy_hp >= player_hp :
               enemy_vX -= 25
            else:
                enemy_vX += 25       

    if enemy_pos.x > screen.get_width() - 100:
        enemy_vX -= 10
            
    if enemy_pos.x <= screen.get_width() / 2 :
        enemy_vX += 30
        
    if enemy_pos.x >= 1280 :
        enemy_vX = -60
        enemy_pos.x = 1279
        
    if enemy_pos.x <= 0:
        enemy_vX = 60
        enemy_pos.x = 1
    
    enemy_pos.x += enemy_vX * dt
    
    if enemy_vX > 0:
        enemy_vX -= 3
    elif enemy_vX < 0:
        enemy_vX += 3
    
    #---------------------------
    
    # ui display
    #---------------------------
    
    draw_hp_bar(screen, 50, 10, player_hp, max_hp, "blue")
    draw_hp_bar(screen, 1030, 10, enemy_hp, max_hp, "red")

    #---------------------------

# -----------------------------------------------------
    pygame.display.flip()
        
pygame.quit()
