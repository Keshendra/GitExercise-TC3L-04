import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shark Attack: Collect Oxygen stones")

clock = pygame.time.Clock()

# Load images
player_image = pygame.image.load('sun_moving_1.png')
stone_image = pygame.image.load('water_stone.png')  # Oxygen stone image
background_image = pygame.image.load('water_bg.png')
heart_image = pygame.image.load('heart.png')

player_width, player_height = 100, 150
player_image = pygame.transform.scale(player_image, (player_width, player_height))
stone_image = pygame.transform.scale(stone_image, (60, 60))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
heart_image = pygame.transform.scale(heart_image, (40, 40))

# Load shark sprite sheet
shark_sprites = [pygame.image.load(f'shark_right_000{i}.png').convert_alpha() for i in range(1, 6)]
shark_sprites = [pygame.transform.scale(img, (200, 100)) for img in shark_sprites]


player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 150
player_speed = 5
player_jump = False
jump_height = 25
double_jump_height = 30  # Higher jump for double jump
gravity = 1
jump_velocity = 0
fall_speed = 15
ground_level = SCREEN_HEIGHT - player_height
double_jump = False

# Shark settings
shark_speed = 3  # Slowed down shark speed
shark_count = 4  # Maximum sharks on screen
sharks = [
    {'rect': pygame.Rect(random.randint(0, SCREEN_WIDTH), random.randint(50, SCREEN_HEIGHT - 200), 200, 80),
     'frame': 0, 'frame_count': 0}
    for _ in range(shark_count)
]

# Function to generate a random stone
def generate_stone():
    stone_x = random.randint(50, SCREEN_WIDTH - 110)
    stone_y = random.randint(100, SCREEN_HEIGHT - 300)
    return pygame.Rect(stone_x, stone_y, 60, 60)

# Generate initial stones
stones = [generate_stone() for _ in range(5)]
total_stones = 30
stone_collected = 0

lives = 3
game_over = False
win_game = False  # New variable to check win condition

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not win_game:  # Check for game state
        # Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Handle jumping
        if keys[pygame.K_UP]:
            if not player_jump:  # If not jumping, start the jump
                player_jump = True
                jump_velocity = jump_height
                double_jump = True  # Allow for a double jump
            elif double_jump:  # If in the air, use the double jump
                jump_velocity = double_jump_height
                double_jump = False  # Disable further jumps

        # Handle jumping and falling
        if player_jump:
            player_y -= jump_velocity
            jump_velocity -= gravity
            if player_y >= ground_level:  # Check if player has landed
                player_y = ground_level
                player_jump = False
                jump_velocity = 0  # Reset jump velocity
                double_jump = False  # Reset double jump
        else:  # If not jumping, apply gravity
            player_y += fall_speed
            if player_y > ground_level:  # Ensure player doesn't go below ground
                player_y = ground_level
                player_jump = False
                jump_velocity = 0  # Reset jump velocity
                double_jump = False  # Reset double jump

        # Boundary checks
        player_x = max(0, min(player_x, SCREEN_WIDTH - player_width))

        # Move sharks and animate
        for shark in sharks:
            shark['rect'].x -= shark_speed
            if shark['rect'].right < 0:
                shark['rect'].x = SCREEN_WIDTH + random.randint(50, 200)
                shark['rect'].y = random.randint(50, SCREEN_HEIGHT - 200)
                shark['frame'] = 0  # Reset frame when repositioning

            # Update frame for animation
            shark['frame_count'] += 1
            if shark['frame_count'] >= 8:  # Change frame every 8 ticks
                shark['frame'] = (shark['frame'] + 1) % len(shark_sprites)
                shark['frame_count'] = 0

        # Check if player collects stones
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for stone in stones[:]:
            if player_rect.colliderect(stone):
                stones.remove(stone)
                stone_collected += 1
                # Spawn a new stone
                stones.append(generate_stone())

        # Check for win condition
        if stone_collected >= total_stones:
            win_game = True  # Set win condition

        # Shark collision and game over check
        for shark in sharks:
            if player_rect.colliderect(shark['rect']):
                lives -= 1
                sharks.remove(shark)  # Remove the shark to avoid repeated collisions
                if lives == 0:
                    game_over = True
                break  # Exit the loop after a collision

    # Drawing
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    # Draw sharks
    for shark in sharks:
        screen.blit(shark_sprites[shark['frame']], (shark['rect'].x, shark['rect'].y))

    # Draw stones
    for stone in stones:
        screen.blit(stone_image, (stone.x, stone.y))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw lives
    for i in range(lives):
        screen.blit(heart_image, (10 + i * 50, 10))

    # Draw collected stones text
    font = pygame.font.Font(None, 36)
    stone_text = font.render(f'Oxygen stones Collected: {stone_collected}/{total_stones}', True, WHITE)
    screen.blit(stone_text, (SCREEN_WIDTH - 400, 10))

    # Check and display game over screen
    if game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('Game Over', True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Check and display win screen
    if win_game:
        font = pygame.font.Font(None, 72)
        win_text = font.render('You Win!', True, RED)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)
