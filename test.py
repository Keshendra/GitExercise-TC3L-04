import pygame
import sys
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

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shark Attack: Collect Oxygen Bubbles")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images
player_image = pygame.image.load('sun_moving_1.png')
bubble_image = pygame.image.load('water_stone.png')  # Oxygen bubble image
background_image = pygame.image.load('water_bg.png')
heart_image = pygame.image.load('heart.png')
bullet_image = pygame.image.load('spike.png')  # Bullet image

# Resize images if necessary
player_width, player_height = 100, 150
player_image = pygame.transform.scale(player_image, (player_width, player_height))
bubble_image = pygame.transform.scale(bubble_image, (60, 60))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
heart_image = pygame.transform.scale(heart_image, (40, 40))
bullet_image = pygame.transform.scale(bullet_image, (20, 10))  # Resize bullet image

# Load left and right shark sprite sheets
left_shark_sprites = [pygame.image.load(f'shark_right_000{i}.png').convert_alpha() for i in range(1, 12)]
right_shark_sprites = [pygame.image.load(f'shark_000{i}.png').convert_alpha() for i in range(1, 12)]
left_shark_sprites = [pygame.transform.scale(img, (200, 120)) for img in left_shark_sprites]
right_shark_sprites = [pygame.transform.scale(img, (200, 120)) for img in right_shark_sprites]

# Player settings
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 150
player_speed = 5
player_jump = False
jump_height = 25
gravity = 1
jump_velocity = 0
fall_speed = 15
ground_level = SCREEN_HEIGHT - player_height
double_jump = False

# Shark settings
shark_count = 3  # Maximum sharks on screen
sharks = []

for _ in range(shark_count):
    direction = random.choice(['left', 'right'])  # Randomly choose direction
    if direction == 'left':
        x = SCREEN_WIDTH + random.randint(50, 200)
    else:
        x = -200  # Start off-screen to the left
    y = random.randint(100, SCREEN_HEIGHT - 200)
    sharks.append({
        'rect': pygame.Rect(x, y, 200, 120),
        'frame': 0,
        'frame_count': 0,
        'speed': random.uniform(1.5, 3),
        'direction': direction
    })

# Function to generate a random bubble
def generate_bubble():
    bubble_x = random.randint(50, SCREEN_WIDTH - 110)  # Adjusted for bubble size
    bubble_y = random.randint(100, SCREEN_HEIGHT - 300)
    return pygame.Rect(bubble_x, bubble_y, 60, 60)

# Generate initial bubbles
bubbles = [generate_bubble() for _ in range(5)]
total_bubbles = 30
bubble_collected = 0

lives = 3
game_over = False

# Oxygen settings
oxygen_level = 100  # Represents 30 seconds of oxygen
oxygen_decrease_rate = 0.1  # Decrease oxygen by 0.1 per frame
oxygen_timer = pygame.time.get_ticks()

# Bullets list
bullets = []

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Fire a bullet
                bullets.append(pygame.Rect(player_x + player_width // 2 - 10, player_y, 20, 10))  # Position above the player

    if not game_over:
        # Decrease oxygen
        current_time = pygame.time.get_ticks()
        if current_time - oxygen_timer < 30000:  # 30 seconds
            oxygen_level -= oxygen_decrease_rate
        else:
            game_over = True  # Game over if oxygen runs out

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
            elif not double_jump:  # Double jump
                player_jump = True
                jump_velocity = jump_height
                double_jump = True  # Prevent further jumps until reset

        if player_jump:
            player_y -= jump_velocity
            jump_velocity -= gravity
            if jump_velocity < -jump_height:
                player_jump = False
                double_jump = False  # Reset double jump when reaching ground
        else:
            player_y += fall_speed

        # Boundary checks
        player_x = max(0, min(player_x, SCREEN_WIDTH - player_width))
        if player_y > ground_level:
            player_y = ground_level
            player_jump = False
            double_jump = False  # Reset double jump when hitting the ground

        # Move sharks and animate
        for shark in sharks:
            if shark['direction'] == 'left':
                shark['rect'].x -= shark['speed']
                if shark['rect'].right < 0:  # If shark goes off-screen
                    shark['rect'].x = SCREEN_WIDTH + random.randint(50, 200)
                    shark['rect'].y = random.randint(100, SCREEN_HEIGHT - 200)
            else:
                shark['rect'].x += shark['speed']
                if shark['rect'].left > SCREEN_WIDTH:  # If shark goes off-screen
                    shark['rect'].x = -200  # Start off-screen to the left
                    shark['rect'].y = random.randint(100, SCREEN_HEIGHT - 200)

            # Update frame for animation
            shark['frame_count'] += 1
            if shark['frame_count'] >= 8:  # Change frame every 8 ticks
                shark['frame'] = (shark['frame'] + 1) % (len(left_shark_sprites) if shark['direction'] == 'left' else len(right_shark_sprites))
                shark['frame_count'] = 0

        # Check if player collects bubbles
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for bubble in bubbles[:]:
            if player_rect.colliderect(bubble):
                bubbles.remove(bubble)
                bubble_collected += 1
                # Spawn a new bubble
                bubbles.append(generate_bubble())

        # Shark collision and game over check
        for shark in sharks:
            if player_rect.colliderect(shark['rect']):
                lives -= 1
                if lives == 0:
                    game_over = True

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= 10  # Move bullet upwards
            # Check for bullet collision with sharks
            for shark in sharks[:]:
                if bullet.colliderect(shark['rect']):
                    sharks.remove(shark)  # Remove shark
                    bullets.remove(bullet)  # Remove bullet
                    break
            else:
                continue  # Continue if the bullet hasn't hit anything
            break  # Break outer loop if bullet hit a shark

    # Drawing
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    # Draw sharks
    for shark in sharks:
        if shark['direction'] == 'left':
            screen.blit(left_shark_sprites[shark['frame']], (shark['rect'].x, shark['rect'].y))
        else:
            screen.blit(right_shark_sprites[shark['frame']], (shark['rect'].x, shark['rect'].y))

    # Draw bubbles
    for bubble in bubbles:
        screen.blit(bubble_image, (bubble.x, bubble.y))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw lives
    for i in range(lives):
        screen.blit(heart_image, (10 + i * 50, 10))

    # Draw collected bubbles text
    font = pygame.font.Font(None, 36)
    bubble_text = font.render(f'Oxygen Bubbles Collected: {bubble_collected}/{total_bubbles}', True, WHITE)
    screen.blit(bubble_text, (SCREEN_WIDTH - 400, 10))

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet_image, (bullet.x, bullet.y))

    # Draw oxygen bar
    oxygen_bar_length = 300
    oxygen_bar_height = 30
    pygame.draw.rect(screen, RED, (10, 60, oxygen_bar_length, oxygen_bar_height))
    pygame.draw.rect(screen, GREEN, (10, 60, oxygen_bar_length * (oxygen_level / 100), oxygen_bar_height))

    # Game over screen
    if game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('Game Over', True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
