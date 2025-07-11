import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
game_state = "menu"

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
player_alive = True
player_death = 0
player_vX = 0
paddle_width = 20
max_hp = 100
player_hp = max_hp
player_damage = 0
inv_time = 0.2
last_damaged = 0
current_time = 0
respawn_time = 3
player_score = 0


# enemy
enemy_alive = True
enemy_death = 0
enemy_hp = max_hp 
enemy_damage = 0
detection_radius = 100
reaction_time = 0.3
enemy_vX = 0
enemy_last_damaged = 0
enemy_score = 0


# hp system
#------------------------------------
base_damage = 0
speed_damage_mult = 0.003

def calculate_damage(ball_speed, paddle_speed):
    speed_damage = abs(ball_speed - paddle_speed) * speed_damage_mult
    
    total_damage = base_damage + speed_damage
    return round(total_damage)

#------------------------------------

# defining things
#------------------------------------
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
        
def draw_player():
    current_time = pygame.time.get_ticks() / 1000
    is_inv = current_time - last_damaged < inv_time
    
    if is_inv:
        if int(current_time * 10) % 2:
            color = "lightblue"
        else:
            color = "blue"
    else:
        color = "blue"

    pygame.draw.line(screen, color, (player_pos.x, player_pos.y + 40), (player_pos.x, player_pos.y - 40), paddle_width)
    
def draw_enemy():
    current_time = pygame.time.get_ticks() / 1000
    is_inv = current_time - enemy_last_damaged < inv_time
    
    if is_inv:
        if int(current_time * 10) % 2:
            color = "pink"
        else:
            color = "red"
    else:
        color = "red"

    pygame.draw.line(screen, color, (enemy_pos.x, enemy_pos.y + 40), (enemy_pos.x, enemy_pos.y - 40), paddle_width)

def draw_respawn_timer():
    font = pygame.font.Font(None, 36)
    
    if not player_alive:
        time_left = respawn_time - (current_time - player_death)
        if time_left > 0:
            text = font.render(f"Player respawning in: {time_left:.1f}s", True, "blue")
            screen.blit(text, (50, 50))
    
    if not enemy_alive:
        time_left = respawn_time - (current_time - enemy_death)
        if time_left > 0:
            text = font.render(f"Enemy respawning in: {time_left:.1f}s", True, "red")
            screen.blit(text, (800, 50))
            
def draw_score(score_1, score_2):
    font = pygame.font.Font(None, 36)
    
    text = font.render(f"{score_1} : {score_2}", True, "white")
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_width() / 2
    text_rect.y = 50  
    screen.blit(text, text_rect)
    
def draw_menu():
    font = pygame.font.Font(None, 74)
    title = font.render("1D PONG", True, "white")
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 200))
    
    font = pygame.font.Font(None, 36)
    start_text = font.render("Press SPACE to start", True, "gray")
    screen.blit(start_text, (screen.get_width()//2 - start_text.get_width()//2, 400))

def draw_pause_menu():
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(128)
    overlay.fill("black")
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.Font(None, 74)
    pause_text = font.render("PAUSED", True, "white")
    screen.blit(pause_text, (screen.get_width()//2 - pause_text.get_width()//2, 300))
    
    font = pygame.font.Font(None, 36)
    resume_text = font.render("Press P to resume", True, "gray")
    screen.blit(resume_text, (screen.get_width()//2 - resume_text.get_width()//2, 400))
#------------------------------------

# start
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and game_state == "playing":
                game_state = "paused"
            elif event.key == pygame.K_p and game_state == "paused":
                game_state = "playing"
        
    screen.fill("black")
    
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
   
    if game_state == "menu":
        draw_menu()
        if keys[pygame.K_SPACE]:
            game_state = "playing"
   
    elif game_state == "playing":
        # game here
        #-------------------------------------------------------
        
        #ball logic
        #---------------------------
    
        pygame.draw.circle(screen, "white", ball_pos, ball_radius)
    
        last_ball = ball_pos.x - ball_vX * dt
        ball_pos.x += ball_vX * dt

        if ball_pos.x >= 1280 - ball_radius and ball_vX > 0:
            ball_vX *= -1
            player_score += 1
    
        if ball_pos.x <= 0 + ball_radius and ball_vX < 0:
            ball_vX *= -1
            enemy_score += 1
             
        # player colision check
    
        current_time = pygame.time.get_ticks() / 1000
    
        player_left = player_pos.x - paddle_width / 2
        player_right = player_pos.x + paddle_width / 2
    
    
        if player_alive and (player_left - ball_radius <= ball_pos.x <= player_right + ball_radius):
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
     
        if enemy_alive and (enemy_left - ball_radius <= ball_pos.x <= enemy_right + ball_radius):
            if ball_vX < 0 and last_ball > enemy_right:
                if current_time - enemy_last_damaged >= inv_time:
                    enemy_damage = calculate_damage(ball_vX, enemy_vX)
                    enemy_hp = max(0, enemy_hp - enemy_damage)
                    enemy_last_damaged = current_time
                
                ball_vX = abs(ball_vX) + enemy_vX * 0.75
                ball_pos.x = enemy_right + ball_radius
            elif ball_vX > 0 and last_ball < enemy_left:
                if current_time - enemy_last_damaged >= inv_time:
                    enemy_damage = calculate_damage(ball_vX, enemy_vX)
                    enemy_hp = max(0, enemy_hp - enemy_damage)
                    enemy_last_damaged = current_time
                
                ball_vX = -abs(ball_vX) + enemy_vX * 0.75
                ball_pos.x = enemy_left - ball_radius 

        ball_vX = (max(min(ball_vX, 1000), -1000))
        ball_vX *= 1.01
    
        #---------------------------
    
        # player and enemy state check
        #---------------------------
    
        if player_hp <= 0 and player_alive:
            player_alive = False
            player_death = current_time
        if enemy_hp <= 0 and enemy_alive:
            enemy_alive = False
            enemy_death = current_time

        if not player_alive and current_time - player_death >= respawn_time :
            player_alive = True
            player_hp = 100
        
            player_vX = 0
            player_pos = pygame.Vector2(100, screen.get_height() / 2)
        
        if not enemy_alive and current_time - enemy_death >= respawn_time :
            enemy_alive = True
            enemy_hp = 100
        
            enemy_vX = 0
            enemy_pos = pygame.Vector2(screen.get_width() - 100 , screen.get_height() / 2)
        #---------------------------
    
        # player logic
        #---------------------------
        if player_alive:
            draw_player()
    
        if player_alive :
            if keys[pygame.K_a]:
                player_vX -= 30      
        
            if keys[pygame.K_d]:
                player_vX += 30
        
            player_pos.x += player_vX * dt
        
            if player_pos.x >= screen.get_width() / 2 - 50 :
                player_vX -= 50
            if player_pos.x >= screen.get_width() / 2  :
                player_vX -= 100
    
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
        if enemy_alive:
            draw_enemy()
    
        if enemy_alive :
            enemy_ball_distance = abs(ball_pos.x - enemy_pos.x)
            if ball_vX != 0:
                enemy_ball_time = enemy_ball_distance / abs(ball_vX)
            else:
                enemy_ball_time = float('inf')
    
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
            
            if enemy_pos.x <= screen.get_width() / 2  + 50:
                enemy_vX += 50
            if enemy_pos.x <= screen.get_width() / 2  :
                enemy_vX += 100
        
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
    
    elif game_state == "paused":
        # Draw the game state first
        pygame.draw.circle(screen, "white", ball_pos, ball_radius)
        if player_alive:
            draw_player()
        if enemy_alive:
            draw_enemy()
        
        # Draw UI
        draw_hp_bar(screen, 50, 10, player_hp, max_hp, "blue")
        draw_hp_bar(screen, 1030, 10, enemy_hp, max_hp, "red")
        draw_respawn_timer()
        draw_score(player_score, enemy_score)
        
        # Draw pause overlay
        draw_pause_menu()
    
    # UI display for playing state
    if game_state == "playing":
        draw_hp_bar(screen, 50, 10, player_hp, max_hp, "blue")
        draw_hp_bar(screen, 1030, 10, enemy_hp, max_hp, "red")
        draw_respawn_timer()
        draw_score(player_score, enemy_score)

    # -----------------------------------------------------
    pygame.display.flip()

pygame.quit()
