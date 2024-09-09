import pygame
import sys
import random

pygame.init()

screen_width, screen_height = 1200, 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

player_size = 50
player_speed = 5
player_pos = [60, 60] 

player_image = pygame.image.load("hero.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

wall_tile_image = pygame.image.load("tile.jpg").convert_alpha()
wall_tile_image = pygame.transform.scale(wall_tile_image, (60, 60))

exit_image = pygame.image.load("entry_portal.png").convert_alpha()
exit_image = pygame.transform.scale(exit_image, (60, 60))

enemy_image = pygame.image.load("earth_mini.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

heart_image = pygame.image.load("heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (50, 50))  

earth_stone_img = pygame.image.load("earth_stone.png").convert_alpha()
earth_stone_img = pygame.transform.scale(earth_stone_img, (60, 60))

background_image = pygame.image.load("earth_bg.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

collect_sound = pygame.mixer.Sound("collect_sound.wav")

# Map layout
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

tile_size = 60

enemies = [
    {'pos': [4 * tile_size, 4 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])},
    {'pos': [7 * tile_size, 7 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])},
    {'pos': [9 * tile_size, 1 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])},
    {'pos': [2 * tile_size, 8 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])},
    {'pos': [12 * tile_size, 10 * tile_size], 'size': 50, 'dir': random.choice([-1, 1])}
]

enemy_speed = 3 

attack_range = 60 

lives = 3  
score = 0  
required_drops = 30  
enemy_hits = 0  

collected_drops = set()  

def initialize_game_map():
    global game_map

    possible_positions = [(row, col) for row in range(len(game_map)) for col in range(len(game_map[row]))]

    possible_positions = [pos for pos in possible_positions if game_map[pos[0]][pos[1]] == 0 or game_map[pos[0]][pos[1]] == 3]

    random.shuffle(possible_positions)

    # Place water drops while ensuring they are at least one tile apart
    placed_drops = []
    while possible_positions and len(placed_drops) < required_drops:
        pos = possible_positions.pop()
        if all(abs(pos[0] - other[0]) > 1 or abs(pos[1] - other[1]) > 1 for other in placed_drops):
            placed_drops.append(pos)
            # Update the map to include water drops
            game_map[pos[0]][pos[1]] = 0

    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 0 and (row, col) not in placed_drops:
                game_map[row][col] = 3

initialize_game_map()

def draw_background():
    screen.blit(background_image, (0, 0))

def draw_map():
    
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            x, y = col * tile_size, row * tile_size
            if game_map[row][col] == 0:  # Water drop tiles
                if (row, col) not in collected_drops:
                    screen.blit(earth_stone_img, (x, y))  # Draw water drop
            elif game_map[row][col] == 1:  # Wall tiles
                screen.blit(wall_tile_image, (x, y))  # Draw wall tiles
                pygame.draw.rect(screen, BLACK, (x, y, tile_size, tile_size), 1)
            elif game_map[row][col] == 2:  # Exit tiles
                screen.blit(exit_image, (x, y))  # Draw exit tile
            elif game_map[row][col] == 3:  # Placeholder for water drops
                pass

def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy_image, (enemy['pos'][0], enemy['pos'][1]))

def draw_hearts():
    for i in range(lives):
        screen.blit(heart_image, (10 + i * (heart_image.get_width() + 5), 10))  # Adjust spacing as needed

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Water Drops: {score} / {required_drops}", True, WHITE)
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

def collect_water_drop():
    global score
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 0:  # Water drop tile
                water_drop_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(water_drop_rect):
                    game_map[row][col] = -1  # Mark water drop as collected
                    collected_drops.add((row, col))  # Add to collected drops
                    score += 1  # Increase score
                    return  # Exit after collecting one drop


def check_collision(new_pos):
    player_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 1:
                wall_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(wall_rect):
                    return True
    return False

def check_exit_reached():
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 2:
                exit_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(exit_rect):
                    return score >= required_drops
    return False

def check_collision_with_water_drops():
    global score, collected_drops
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 0 and (row, col) not in collected_drops:
                water_drop_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if player_rect.colliderect(water_drop_rect):
                    collected_drops.add((row, col))  # Mark this drop as collected
                    score += 1
                    collect_sound.play()  # Play collect sound effect
                    if score >= required_drops:
                        print("You win!")
                        pygame.quit()
                        sys.exit()

def handle_player_movement():
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
        print("Congratulations! You collected enough water drops and reached the exit!")
        pygame.quit()
        sys.exit()

def check_enemy_collision():
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
    global player_pos, player_speed, collected_drops, lives, score, enemy_hits

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_player_movement()
        move_enemies()  

        draw_background()
        
        
        draw_map()
        draw_enemies()
        draw_hearts()
        draw_score()
        screen.blit(player_image, (player_pos[0], player_pos[1]))  
        
        # Check for collisions
        if check_enemy_collision():
            lives -= 1
            if lives <= 0:
                game_over()
            player_pos = [60, 60]  # Reset player position
        
        check_collision_with_water_drops() 
        
        # Update display
        pygame.display.flip()
        
        # Frame rate control
        clock.tick(30)

if __name__ == "__main__":
    main()
