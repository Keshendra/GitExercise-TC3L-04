import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer with Moving Platforms")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images
player_image = pygame.image.load('hero.png')
platform_image = pygame.image.load('platform2.png')
coin_image = pygame.image.load('stone_water.png')
background_image = pygame.image.load('water_bg.png')
spike_image = pygame.image.load('jellyfish.png')  # Add your own spike image
heart_image = pygame.image.load('heart.png')  # Add your own heart image

# Resize images if necessary
player_width, player_height = 100, 150
player_image = pygame.transform.scale(player_image, (player_width, player_height))  # Increased player size
platform_image = pygame.transform.scale(platform_image, (200, 80))
coin_image = pygame.transform.scale(coin_image, (60, 60))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
spike_image = pygame.transform.scale(spike_image, (80, 80))  # Increased spike size
heart_image = pygame.transform.scale(heart_image, (40, 40))

# Player settings
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 150  # Start higher above the bottom to ensure player visibility
player_speed = 5
player_jump = False
on_platform = False
jump_height = 20
double_jump_height = 25  # Higher for double jump
gravity = 1
jump_velocity = 0
fall_speed = 15  

ground_level = SCREEN_HEIGHT - player_height  

background_x = 0 
background_y = 0

platform_speed = 2  
platforms = [
    pygame.Rect(100, 500, 200, 20),
    pygame.Rect(400, 400, 200, 20),
    pygame.Rect(700, 300, 200, 20),
    pygame.Rect(1000, 200, 200, 20),
]

def generate_coins():
    coins = []
    for platform in platforms:
        num_coins = random.randint(1, 2) 
        for _ in range(num_coins):
            coin_x = platform.x + random.randint(10, platform.width - 70) 
            coin_y = platform.y - 60  
            coins.append({'rect': pygame.Rect(coin_x, coin_y, 60, 60), 'platform': platform})
    return coins

coins = generate_coins()
total_stones = 30 

# Spike settings
spikes = [
    pygame.Rect(400, 580, 80, 80), 
    pygame.Rect(700, 480, 80, 80),  
]

lives = 3
spike_hits = 0 

collected_stones = 0

jump_time = 0
double_jump_time_window = 0.3  

# Main game loop
running = True
game_over = False
while running:
    current_time = time.time() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            if not player_jump:  # First jump
                player_jump = True
                jump_velocity = jump_height
                jump_time = current_time  
            elif current_time - jump_time <= double_jump_time_window: 
                player_jump = True
                jump_velocity = double_jump_height  
                jump_time = 0 

      
        if player_jump:
            player_y -= jump_velocity 
            jump_velocity -= gravity  
            if jump_velocity < -jump_height:  
                player_jump = False
        else:
            # Apply gravity when the player is not jumping
            player_y += fall_speed

        # Boundary checks to keep the player on the screen
        if player_x < 0:
            player_x = 0
        elif player_x > SCREEN_WIDTH - player_width:  
            player_x = SCREEN_WIDTH - player_width
        if player_y > ground_level:  
            player_y = ground_level
            player_jump = False

        # Move platforms, coins, and spikes together to the left and reset when they go off screen
        for platform in platforms:
            platform.x -= platform_speed 
            if platform.right < 0: 
                platform.x = SCREEN_WIDTH 
                
                coins = [coin for coin in coins if coin['platform'] != platform]  # Remove old coins
                num_new_coins = random.randint(1, 2)  # Random number of new coins
                for _ in range(num_new_coins):
                    coin_x = platform.x + random.randint(10, platform.width - 70)
                    coin_y = platform.y - 60
                    coins.append({'rect': pygame.Rect(coin_x, coin_y, 60, 60), 'platform': platform})

        for coin in coins[:]:
            
            coin['rect'].x = coin['platform'].x + 50
            coin['rect'].y = coin['platform'].y - 60 

        for spike in spikes:
            spike.x -= platform_speed  # Move spikes with platforms
            if spike.right < 0:
                spike.x = SCREEN_WIDTH  # Reset spike position

        
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)  
        on_platform = False 
        for platform in platforms:
            if player_rect.colliderect(platform) and player_y + player_height <= platform.y + fall_speed:
                player_y = platform.y - player_height  # Adjust for player size
                on_platform = True
                jump_velocity = 0 

        # Collision detection with coins
        for coin in coins[:]:
            if player_rect.colliderect(coin['rect']):
                coins.remove(coin)
                collected_stones += 1  
                if collected_stones >= total_stones:
                    
                    pass

        # Collision detection with spikes
        for spike in spikes:
            if player_rect.colliderect(spike):
                spike_hits += 1
                if spike_hits == 1:
                    lives -= 1
                    player_x = SCREEN_WIDTH // 2
                    player_y = SCREEN_HEIGHT - 150  # Reset player position
                elif spike_hits == 2:
                    lives -= 1
                    player_x = SCREEN_WIDTH // 2
                    player_y = SCREEN_HEIGHT - 150  # Reset player position
                elif spike_hits >= 3:
                    game_over = True
                break  

    # Drawing
    screen.fill(WHITE)

    # Draw the background (static)
    screen.blit(background_image, (background_x, background_y))

    # Draw platforms
    for platform in platforms:
        screen.blit(platform_image, (platform.x, platform.y))

    # Draw coins
    for coin in coins:
        screen.blit(coin_image, (coin['rect'].x, coin['rect'].y))

    # Draw spikes
    for spike in spikes:
        screen.blit(spike_image, (spike.x, spike.y))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw lives
    for i in range(lives):
        screen.blit(heart_image, (10 + i * 50, 10))

    # Draw collected stones text at the top right corner
    font = pygame.font.Font(None, 36)
    stones_text = font.render(f'Stones Collected: {collected_stones}/{total_stones}', True, WHITE)
    text_rect = stones_text.get_rect()
    text_rect.topright = (SCREEN_WIDTH - 10, 10)  # Position text at the top right corner
    screen.blit(stones_text, text_rect)

    if game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('Game Over', True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds before quitting
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)  # Frame rate
