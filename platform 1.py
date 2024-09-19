import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 1200, 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fire Dungeon")

# Clock to control frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
player_size = 50
player_speed = 5
player_pos = [60, 60]  # Start position on the first tile

# Load images
player_image = pygame.image.load("sun_moving.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

wall_tile_image = pygame.image.load("lava tile.png").convert_alpha()
wall_tile_image = pygame.transform.scale(wall_tile_image, (60, 60))

exit_image = pygame.image.load("fire portal.png").convert_alpha()
exit_image = pygame.transform.scale(exit_image, (60, 60))

enemy_image = pygame.image.load("fire_mini.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

heart_image = pygame.image.load("fire health.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (50, 50))  # Increased heart size

# Load fire drop image
fire_drop_image = pygame.image.load("fire_stone.png").convert_alpha()
fire_drop_image = pygame.transform.scale(fire_drop_image, (60, 60))

# Load static background image
background_image = pygame.image.load("fire bg.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Map layout
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 2, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

tile_size = 60

# Enemy settings
enemies = [
    {'pos': [4 * tile_size, 4 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])},
    {'pos': [7 * tile_size, 7 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])},
    {'pos': [9 * tile_size, 1 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])},
    {'pos': [2 * tile_size, 8 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])},
    {'pos': [12 * tile_size, 10 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])}
]

enemy_speed = 2  # Speed of enemy movement

# Attack settings
attack_range = 60  # The range within which the attack is effective

# Player lives settings
lives = 3  # Set to 3 hearts
score = 0  # Initialize score
required_flames = 5  # Number of flames required to exit the game
enemy_hits = 0  # Track number of hits by enemies

# Keep track of collected fire flames
collected_flames = set()  # Use a set to store coordinates of collected flames

def initialize_game_map():
    """Initialize the game map with fire flames ensuring they are at least one tile apart."""
    global game_map

    # Create a list of all possible positions for fire flames
    possible_positions = [(row, col) for row in range(len(game_map)) for col in range(len(game_map[row]))]

    # Remove positions that are not valid for placing fire flames (i.e., walls or exit)
    possible_positions = [pos for pos in possible_positions if game_map[pos[0]][pos[1]] == 0 or game_map[pos[0]][pos[1]] == 3]

    # Shuffle positions to randomize
    random.shuffle(possible_positions)

    # Place fire flames while ensuring they are at least one tile apart
    placed_flames = []
    while possible_positions and len(placed_flames) < required_flames:
        pos = possible_positions.pop()
        if all(abs(pos[0] - other[0]) > 1 or abs(pos[1] - other[1]) > 1 for other in placed_flames):
            placed_flames.append(pos)
            # Update the map to include fire flames
            game_map[pos[0]][pos[1]] = 0

    # Set the remaining positions to the default (fire drop placeholder)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 0 and (row, col) not in placed_flames:
                game_map[row][col] = 3  # Mark these as the non-fire drop tiles

initialize_game_map()

def draw_background():
    """Draw the static background image on the screen."""
    screen.blit(background_image, (0, 0))

def draw_map():
    """Draws the game map on the screen using the appropriate tile image."""
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            x, y = col * tile_size, row * tile_size
            if game_map[row][col] == 0:  # fire drop tiles
                if (row, col) not in collected_flames:
                    screen.blit(fire_drop_image, (x, y))  # Draw fire drop
            elif game_map[row][col] == 1:  # Wall tiles
                screen.blit(wall_tile_image, (x, y))  # Draw wall tiles
                pygame.draw.rect(screen, BLACK, (x, y, tile_size, tile_size), 1)
            elif game_map[row][col] == 2:  # Exit tiles
                screen.blit(exit_image, (x, y))  # Draw exit tile
            elif game_map[row][col] == 3:  # Placeholder for fire flames
                pass

def draw_enemies():
    """Draw enemies on the screen."""
    for enemy in enemies:
        screen.blit(enemy_image, (enemy['pos'][0], enemy['pos'][1]))

def draw_hearts():
    """Draw lives (hearts) on the screen."""
    for i in range(lives):
        screen.blit(heart_image, (10 + i * (heart_image.get_width() + 5), 10))  # Adjust spacing as needed

def draw_score():
    """Draws the score as fire flames collected / required flames at the top right of the screen."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Fire Flames: {score} / {required_flames}", True, WHITE)
    screen.blit(score_text, (screen_width - 300, 10))

def move_enemies():
    """Move enemies and handle collision with player."""
    global enemy_hits

    for enemy in enemies:
        enemy['pos'][0] += enemy['dir'] * enemy_speed
        if enemy['pos'][0] < 0 or enemy['pos'][0] > screen_width - enemy['size']:
            enemy['dir'] *= -1

        # Check for collision with player
        enemy_rect = pygame.Rect(enemy['pos'][0], enemy['pos'][1], enemy['size'], enemy['size'])
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

        if enemy_rect.colliderect(player_rect):
            enemy_hits += 1
            if enemy_hits >= 3:  # Number of hits after which player loses a life
                global lives
                lives -= 1
                if lives <= 0:
                    game_over()
                player_pos[:] = [60, 60]  # Reset player position
                enemy_hits = 0

def collect_fire_drop():
    """Handle fire drop collection."""
    global score
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 0:  # fire drop tile
                fire_drop_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(fire_drop_rect):
                    game_map[row][col] = -1  # Mark fire drop as collected
                    collected_flames.add((row, col))  # Add to collected flames
                    score += 1  # Increase score
                    return  # Exit after collecting one drop

def check_collision(new_pos):
    """Check if the player collides with any wall tiles."""
    player_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 1:
                wall_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(wall_rect):
                    return True
    return False

def check_exit_reached():
    """Check if the player reaches the exit and has collected enough fire flames."""
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 2:
                exit_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(exit_rect):
                    return score >= required_flames
    return False

def handle_player_movement():
    """Handles the player's movement based on keyboard input."""
    keys = pygame.key.get_pressed()
    new_pos = list(player_pos)

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
        print("Congratulations! You collected enough flames and reached the exit!")
        pygame.quit()
        sys.exit()

def check_enemy_collision():
    """Check if player collides with enemies."""
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy['pos'][0], enemy['pos'][1], enemy['size'], enemy['size'])
        if player_rect.colliderect(enemy_rect):
            return True
    return False

def game_over():
    """Handle game over state."""
    print("Game Over")
    pygame.quit()
    sys.exit()

def main():
    global player_pos, player_speed, collected_flames, lives, score, enemy_hits

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement handling
        handle_player_movement()
        move_enemies()  # Update enemy positions

        # Fill screen with background color
        draw_background()
        
        # Draw everything
        draw_map()
        draw_enemies()
        
        draw_hearts()
        draw_score()
        screen.blit(player_image, (player_pos[0], player_pos[1]))  # Draw player
        
        # Check for collisions
        if check_enemy_collision():
            lives -= 1
            if lives <= 0:
                game_over()
            player_pos = [60, 60]  # Reset player position
        
        collect_fire_drop()  # Check and handle fire flame collection
        
        # Update display
        pygame.display.flip()
        
        # Frame rate control
        clock.tick(30)

if __name__ == "__main__":
    main()
