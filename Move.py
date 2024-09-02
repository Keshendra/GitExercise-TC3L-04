import pygame
import math
import random
import sys

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Answer And Move")

bg = pygame.image.load("moving_bg2.jpg").convert()
bg_width = bg.get_width()

hero_standing = pygame.image.load("hero.png").convert_alpha()
hero_jumping = pygame.image.load("hero_jump.png").convert_alpha()
hero_ducking = pygame.image.load("hero_duck.png").convert_alpha()

hero_width = int(hero_standing.get_width() * 0.75)
hero_height = int(hero_standing.get_height() * 0.75)
hero_standing = pygame.transform.scale(hero_standing, (hero_width, hero_height))
hero_jumping = pygame.transform.scale(hero_jumping, (hero_width, hero_height))
hero_ducking = pygame.transform.scale(hero_ducking, (hero_width, hero_height // 2))

current_hero_image = hero_standing

obstacle = pygame.image.load("obstacle.png").convert_alpha()
obstacle = pygame.transform.scale(obstacle, (150, 150)) 
obstacle_width = obstacle.get_width()
obstacle_height = obstacle.get_height()

scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

hero_x = 100
hero_y = SCREEN_HEIGHT - hero_height - 50
hero_speed = 5
hero_moving = False
jumping = False
ducking = False

jump_velocity = 32
gravity = 1 


obstacle_x = SCREEN_WIDTH
obstacle_y = (SCREEN_HEIGHT - obstacle_height) // 2  
obstacle_speed = 4  


obstacle_counter = 0  
total_obstacles = 10 
num_trigger_obstacles = 4 
trigger_obstacles = [] 
show_lose_message = False

start_ticks = pygame.time.get_ticks() 

# Font settings
font = pygame.font.SysFont('Times New Roman', 40, bold=True)  
lose_font = pygame.font.SysFont('Times New Roman', 100, bold=True) 
button_font = pygame.font.SysFont('Arial', 50)  

button_color = (0, 200, 0)
button_hover_color = (0, 255, 0)
button_width = 300
button_height = 100
button_rect = pygame.Rect(
    (SCREEN_WIDTH - button_width) // 2,
    (SCREEN_HEIGHT) // 2 + 50,
    button_width,
    button_height
)
button_text = "Play Again"

def reset_game():
  #game restart aagum
    global hero_x, hero_y, scroll, obstacle_x, obstacle_y, obstacle_speed
    global obstacle_counter, show_lose_message, start_ticks, jump_velocity, trigger_obstacles

    hero_x = 100
    hero_y = SCREEN_HEIGHT - hero_height - 50
    scroll = 0
    obstacle_x = SCREEN_WIDTH
    obstacle_y = (SCREEN_HEIGHT - obstacle_height) // 2
    obstacle_speed = 4
    obstacle_counter = 0
    show_lose_message = False
    start_ticks = pygame.time.get_ticks()
    jump_velocity = 38

    # ella levelkum randomize pannum obstacle
    trigger_obstacles = random.sample(range(1, total_obstacles + 1), num_trigger_obstacles)
    print(f"New trigger obstacles: {trigger_obstacles}")  

def draw_lose_screen():
   #lose screen 
    screen.fill((0, 0, 0)) 

   # YOU LOSE text
    lose_text = lose_font.render("YOU LOSE !", True, (255, 0, 0))  # Red bold text
    lose_text_rect = lose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(lose_text, lose_text_rect)

    
    mouse_pos = pygame.mouse.get_pos()

    if button_rect.collidepoint(mouse_pos):
        current_button_color = button_hover_color
    else:
        current_button_color = button_color

    # button draw
    pygame.draw.rect(screen, current_button_color, button_rect, border_radius=10)

    
    button_label = button_font.render(button_text, True, (255, 255, 255))
    button_label_rect = button_label.get_rect(center=button_rect.center)
    screen.blit(button_label, button_label_rect)

    pygame.display.update()

# Game loop
run = True
game_state = "playing"  

while run:
    clock.tick(FPS)

    if game_state == "playing":
      
        for i in range(tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))

        scroll -= 2
        if abs(scroll) > bg_width:
            scroll = 0

        # hero jump duck
        if jumping:
            hero_y -= jump_velocity
            jump_velocity -= gravity
            current_hero_image = hero_jumping
            if jump_velocity < -32:
                jumping = False
                jump_velocity = 32
        elif ducking:
            hero_y = SCREEN_HEIGHT - (hero_height // 2) - 50
            current_hero_image = hero_ducking
        else:
            hero_y = SCREEN_HEIGHT - hero_height - 50
            current_hero_image = hero_standing

        
        obstacle_x -= obstacle_speed
        if obstacle_x < -obstacle_width:
            obstacle_x = SCREEN_WIDTH
            obstacle_y = (SCREEN_HEIGHT - obstacle_height) // 2 
            obstacle_speed += 1.0 
            obstacle_counter += 1  #obstacle ode scale maaturathu

        screen.blit(current_hero_image, (hero_x, hero_y))
        screen.blit(obstacle, (obstacle_x, obstacle_y))

        hero_rect = pygame.Rect(hero_x, hero_y, hero_width, hero_height)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

        if hero_rect.colliderect(obstacle_rect):
            if obstacle_counter in trigger_obstacles:
                print(f"Collision detected with obstacle {obstacle_counter}! Trigger puzzle.")
                
                run = False  
            else:
                print(f"Collision detected with obstacle {obstacle_counter}! You lose.")
                game_state = "game_over" 

        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000 
        timer_text = font.render(f"Time: {elapsed_time}s", True, (255, 255, 255)) 
        screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))  

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    hero_moving = True
                if event.key == pygame.K_UP and not jumping:
                    jumping = True
                    ducking = False
                if event.key == pygame.K_DOWN and not jumping:
                    ducking = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    hero_moving = False
                if event.key == pygame.K_DOWN:
                    ducking = False

        pygame.display.update()

    elif game_state == "game_over":
        draw_lose_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    reset_game()
                    game_state = "playing"


pygame.quit()
sys.exit()
