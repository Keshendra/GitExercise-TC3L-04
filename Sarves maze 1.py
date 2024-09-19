import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

# Colors
WHITE = (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("fire")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images with error handling
try:
    player_image = pygame.image.load('sun_moving.png')
    platform_image = pygame.image.load('lava tile.png')
    coin_image = pygame.image.load('fire_stone.png')
    background_image = pygame.image.load('fire background.png')
except pygame.error as e:
    print(f"Unable to load image: {e}")
    sys.exit()

# Resize images if necessary
player_width, player_height = 150, 100
player_image = pygame.transform.scale(player_image, (player_width, player_height))  # Player size
platform_image = pygame.transform.scale(platform_image, (200, 80))
coin_image = pygame.transform.scale(coin_image, (60, 60))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sound with error handling
try:
    collect_sound = pygame.mixer.Sound('coin collect.mp3')
    pygame.mixer.music.load('fire music.mp3')  # Load background music
    pygame.mixer.music.set_volume(0.5)  # Set volume level (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play music indefinitely
except pygame.error as e:
    print(f"Unable to load sound or music: {e}")
    sys.exit()

# Player settings
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 150  # Start higher above the bottom to ensure player visibility
player_speed = 5
player_jump = False
jump_height = 18
gravity = 1
jump_velocity = 0
falling = True  # Start as falling until on a platform or ground

# Background settings (Static)
background_x = 0
background_y = 0

# Platform settings with a more interesting arrangement
platforms = [
    pygame.Rect(100, 600, 200, 20),  # Platform 1
    pygame.Rect(400, 450, 200, 20),  # Platform 2
    pygame.Rect(750, 500, 200, 20),  # Platform 3 (a little higher)
    pygame.Rect(1100, 400, 200, 20), # Platform 4
    pygame.Rect(550, 300, 200, 20)   # Platform 5 (much higher)
]

# Coin settings (attach coins to specific platforms)
coins = [
    {'rect': pygame.Rect(150, platforms[0].y - 60, 60, 60), 'platform': platforms[0]},
    {'rect': pygame.Rect(450, platforms[1].y - 60, 60, 60), 'platform': platforms[1]},
    {'rect': pygame.Rect(800, platforms[2].y - 60, 60, 60), 'platform': platforms[2]},
    {'rect': pygame.Rect(1150, platforms[3].y - 60, 60, 60), 'platform': platforms[3]},
    {'rect': pygame.Rect(600, platforms[4].y - 60, 60, 60), 'platform': platforms[4]}
]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP] and not player_jump and not falling:  # Jump only if not already jumping or falling
        player_jump = True
        jump_velocity = jump_height

    # Jumping mechanics
    if player_jump:
        player_y -= jump_velocity
        jump_velocity -= gravity
        if jump_velocity < -jump_height:
            player_jump = False
            falling = True

    # Gravity effect
    if not player_jump:
        player_y += gravity

    # Platform collision logic (to stand on platforms)
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    on_platform = False  # Track if the player is standing on a platform

    for platform in platforms:
        if player_rect.colliderect(platform) and player_y + player_height <= platform.y + player_speed:
            player_y = platform.y - player_height
            falling = False
            on_platform = True
            jump_velocity = 0  # Reset jump velocity when standing on a platform
            break

    if not on_platform and not player_jump:
        falling = True

    # Boundary checks to keep the player on the screen
    if player_x < 0:
        player_x = 0
    elif player_x > SCREEN_WIDTH - player_width:
        player_x = SCREEN_WIDTH - player_width
    if player_y > SCREEN_HEIGHT - player_height:
        player_y = SCREEN_HEIGHT - player_height
        falling = False  # Stop falling when hitting the bottom of the screen

    # Move platforms and coins together to the left and reset when they go off screen
    for platform in platforms:
        platform.x -= 5
        if platform.right < 0:
            platform.x = SCREEN_WIDTH
            platform.y = 250 + (platforms.index(platform) * 100)

    for coin in coins:
        coin['rect'].x = coin['platform'].x + 50
        coin['rect'].y = coin['platform'].y - 60

    # Collision detection with coins
    for coin in coins[:]:
        if player_rect.colliderect(coin['rect']):
            collect_sound.play()  # Play the sound effect
            coins.remove(coin)

    # Drawing
    screen.fill(WHITE)
    screen.blit(background_image, (background_x, background_y))

    # Draw platforms
    for platform in platforms:
        screen.blit(platform_image, (platform.x, platform.y))

    # Draw coins
    for coin in coins:
        screen.blit(coin_image, (coin['rect'].x, coin['rect'].y))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    pygame.display.flip()
    clock.tick(30)
