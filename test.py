import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 1200, 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")

# Clock to control frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
player_size = 50
player_speed = 5

# Load images
player_image = pygame.image.load("hero.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

wall_tile_image = pygame.image.load("tile.jpg").convert_alpha()
wall_tile_image = pygame.transform.scale(wall_tile_image, (60, 60))

exit_image = pygame.image.load("img_2.png").convert_alpha()
exit_image = pygame.transform.scale(exit_image, (60, 60))

background_image = pygame.image.load("earth_bg.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

obstacle_image = pygame.image.load("earth_mini.png").convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (60, 60))  # Assuming obstacles are 60x60

tile_size = 60

# Map layout with obstacles and the exit (2)
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 2, 1],  # Exit at bottom-right corner
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Initialize moving obstacles
num_obstacles = 3
obstacle_speed = 2

# Create moving obstacles
moving_obstacles = []
for _ in range(num_obstacles):
    x, y = random.randint(0, screen_width - tile_size), random.randint(0, screen_height - tile_size)
    dx, dy = random.choice([-1, 1]), random.choice([-1, 1])
    moving_obstacles.append({'rect': pygame.Rect(x, y, tile_size, tile_size), 'dx': dx, 'dy': dy})

def draw_map():
    """Draws the game map on the screen using the appropriate tile image."""
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            x, y = col * tile_size, row * tile_size
            if game_map[row][col] == 1:
                screen.blit(wall_tile_image, (x, y))
                pygame.draw.rect(screen, BLACK, (x, y, tile_size, tile_size), 1)  # Draw wall border
            elif game_map[row][col] == 2:
                screen.blit(exit_image, (x, y))

def check_collision(new_pos):
    """Check if the player collides with any wall tiles or moving obstacles."""
    player_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
    
    # Check collision with walls
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 1:
                wall_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(wall_rect):
                    return True
    
    # Check collision with moving obstacles
    for obstacle in moving_obstacles:
        if player_rect.colliderect(obstacle['rect']):
            return True

    return False

def check_exit_reached():
    """Check if the player reaches the exit."""
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 2:
                exit_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(exit_rect):
                    return True
    return False

def handle_player_movement():
    """Handles the player's movement based on keyboard input."""
    keys = pygame.key.get_pressed()  # Detect key press

    new_pos = list(player_pos)  # Copy the current position

    if keys[pygame.K_LEFT]:
        new_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        new_pos[0] += player_speed
    if keys[pygame.K_UP]:
        new_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        new_pos[1] += player_speed

    if not check_collision(new_pos):
        player_pos[0], player_pos[1] = new_pos

    if check_exit_reached():
        print("Congratulations! You reached the exit!")
        pygame.quit()
        sys.exit()

def update_obstacles():
    """Update the position of moving obstacles."""
    for obstacle in moving_obstacles:
        obstacle['rect'].x += obstacle['dx'] * obstacle_speed
        obstacle['rect'].y += obstacle['dy'] * obstacle_speed

        # Bounce off the edges of the screen
        if obstacle['rect'].left < 0 or obstacle['rect'].right > screen_width:
            obstacle['dx'] *= -1
        if obstacle['rect'].top < 0 or obstacle['rect'].bottom > screen_height:
            obstacle['dy'] *= -1

# Initial player position
player_pos = [tile_size, tile_size]

# Game loop
while True:
    screen.blit(background_image, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Handle player movement
    handle_player_movement()
    
    # Update obstacles
    update_obstacles()
    
    # Draw map, moving obstacles, and player
    draw_map()
    for obstacle in moving_obstacles:
        screen.blit(obstacle_image, obstacle['rect'])  # Draw obstacle image
    
    screen.blit(player_image, player_pos)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(30)