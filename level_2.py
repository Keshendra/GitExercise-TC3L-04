import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Answer And Move")

bg = pygame.image.load("level_2.jpg").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the background to fit the screen
bg_width = bg.get_width()

hero = pygame.image.load("hero_boat.png").convert_alpha()

hero_width = int(hero.get_width() * 0.75)
hero_height = int(hero.get_height() * 0.75)

hero = pygame.transform.scale(hero, (hero_width, hero_height))

current_hero_image = hero

obstacle = pygame.image.load("bird.png").convert_alpha()
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

jump_velocity = 38
gravity = 1.5

obstacle_x = SCREEN_WIDTH
obstacle_y = (SCREEN_HEIGHT - obstacle_height) // 2 
obstacle_speed = 4 

start_ticks = pygame.time.get_ticks()
font = pygame.font.SysFont('Times New Roman', 40, bold=True)  # Increase font size and boldness

# Game loop
run = True
while run:
    clock.tick(FPS)

    # Draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    scroll -= 2
    if abs(scroll) > bg_width:
        scroll = 0

    if jumping:
        hero_y -= jump_velocity
        jump_velocity -= gravity
        if jump_velocity < -38:  
            jumping = False
            jump_velocity = 38
    elif ducking:
        hero_y = SCREEN_HEIGHT - (hero_height // 2) - 50
    else:
        hero_y = SCREEN_HEIGHT - hero_height - 50

    # Move the obstacle towards the player
    obstacle_x -= obstacle_speed
    if obstacle_x < -obstacle_width:
        obstacle_x = SCREEN_WIDTH
        obstacle_y = (SCREEN_HEIGHT - obstacle_height) // 2  
        obstacle_speed += 0.3

    # Draw hero and obstacle
    screen.blit(current_hero_image, (hero_x, hero_y))
    screen.blit(obstacle, (obstacle_x, obstacle_y))

    # Check for collision with the obstacle
    hero_rect = pygame.Rect(hero_x, hero_y, hero_width, hero_height if not ducking else hero_height // 2)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

    if hero_rect.colliderect(obstacle_rect):
        print("Collision detected! Trigger puzzle.")
        run = False 

    # Display timer
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  
    timer_text = font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))  
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))  

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not jumping:
                jumping = True
                ducking = False
            if event.key == pygame.K_DOWN and not jumping:
                ducking = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                ducking = False

    pygame.display.update()

pygame.quit()
