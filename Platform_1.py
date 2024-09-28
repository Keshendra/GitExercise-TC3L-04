import pygame
import sys
import time
import random

pygame.init()
   
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

clock = pygame.time.Clock()

# Load images
platform_image = pygame.image.load('tiles1.png')
stone_image = pygame.image.load('stone_earth.png')
background_image = pygame.image.load('earth_bg.jpg')

# Load sound
stone_collect_sound = pygame.mixer.Sound('collect_sound.wav')

# Resize images if necessary
player_width, player_height = 150, 150
player_images = [pygame.image.load(f"sun_moving_{i}.png").convert_alpha() for i in range(1, 10)]
player_images = [pygame.transform.scale(img, (player_width, player_height)) for img in player_images]

platform_image = pygame.transform.scale(platform_image, (200, 80))
stone_image = pygame.transform.scale(stone_image, (60, 60))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player settings
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 150  
player_speed = 4
player_jump = False
jump_height = 20
gravity = 1
jump_velocity = 0
fall_speed = 15  

ground_level = SCREEN_HEIGHT - player_height 

platform_speed = 4
platforms = [
    pygame.Rect(100, 500, 200, 20),
    pygame.Rect(400, 400, 200, 20),
    pygame.Rect(700, 300, 200, 20),
    pygame.Rect(1000, 200, 200, 20),
]

# Stone settings (Attach random number of stones to platforms)
def generate_stones():
    stones = []
    for platform in platforms:
        num_stones = random.randint(1, 2) 
        for _ in range(num_stones):
            stone_x = platform.x + random.randint(10, platform.width - 70) 
            stone_y = platform.y - 60  
            stones.append({'rect': pygame.Rect(stone_x, stone_y, 60, 60), 'platform': platform})
    return stones

stones = generate_stones()
total_stones = 30  

# Collected stones
collected_stones = 0

# Timer settings
start_time = time.time()
time_limit = 30  # 30 seconds

current_frame = 0
frame_delay = 5 
frame_counter = 0

# Main game loop
running = True
game_over = False
win = False  # New win state
while running:
    current_time = time.time()  
    elapsed_time = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not win:  # Check if the game is ongoing
        # Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            if not player_jump: 
                player_jump = True
                jump_velocity = jump_height

        # Gravity and jump mechanics
        if player_jump:
            player_y -= jump_velocity  
            jump_velocity -= gravity  
            if jump_velocity < 0:  
                player_jump = False
        else:
            player_y += fall_speed

        # Prevent jumping off the screen
        if player_y < 0:  
            player_y = 0
        elif player_y > ground_level: 
            player_y = ground_level
            player_jump = False
            jump_velocity = 0

        # Boundary checks for left and right movement
        if player_x < 0:
            player_x = 0
        elif player_x > SCREEN_WIDTH - player_width:
            player_x = SCREEN_WIDTH - player_width

        # Move platforms and stones together to the left and reset when they go off screen
        for platform in platforms:
            platform.x -= platform_speed 
            if platform.right < 0: 
                platform.x = SCREEN_WIDTH  
                
                stones = [stone for stone in stones if stone['platform'] != platform]  
                num_new_stones = random.randint(1, 2)  
                for _ in range(num_new_stones):
                    stone_x = platform.x + random.randint(10, platform.width - 70)
                    stone_y = platform.y - 60
                    stones.append({'rect': pygame.Rect(stone_x, stone_y, 60, 60), 'platform': platform})

        for stone in stones[:]:
            stone['rect'].x = stone['platform'].x + 50
            stone['rect'].y = stone['platform'].y - 60  

        # Collision detection with platforms
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height) 
        on_platform = False  
        for platform in platforms:
            if player_rect.colliderect(platform) and player_y + player_height <= platform.y + fall_speed:
                player_y = platform.y - player_height  
                on_platform = True
                jump_velocity = jump_height  
                break  

        # Collision detection with stones
        for stone in stones[:]:
            if player_rect.colliderect(stone['rect']):
                stones.remove(stone)
                collected_stones += 1  
                stone_collect_sound.play()  # Play sound on stone collection
                if collected_stones >= total_stones:
                    win = True  # Set win state

        # Check if time is up
        if elapsed_time >= time_limit:
            game_over = True

    # Drawing
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    for platform in platforms:
        screen.blit(platform_image, (platform.x, platform.y))

    for stone in stones:
        screen.blit(stone_image, (stone['rect'].x, stone['rect'].y))

    frame_counter += 1
    if frame_counter >= frame_delay:
        current_frame = (current_frame + 1) % len(player_images)
        frame_counter = 0
    
    screen.blit(player_images[current_frame], (player_x, player_y))

    # Display collected stones
    font = pygame.font.SysFont(None, 36)
    collected_text = font.render(f"Collected Stones: {collected_stones}/{total_stones}", True, WHITE)
    text_rect = collected_text.get_rect()
    text_rect.topright = (SCREEN_WIDTH - 10, 10)  
    screen.blit(collected_text, text_rect)

    # Display timer
    remaining_time = max(0, time_limit - int(elapsed_time))
    timer_text = font.render(f"Time Remaining: {remaining_time}", True, WHITE)
    screen.blit(timer_text, (10, 10))

    # Check game over or win state
    if game_over:
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
    elif win:  # Display win message
        win_font = pygame.font.SysFont(None, 72)
        win_text = win_font.render("YOU WIN!", True, RED)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
