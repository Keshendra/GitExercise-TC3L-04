import pygame
import sys
import time
import random
import moviepy.editor as mp
import numpy as np

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()  # Ensure the mixer is initialized

# Set up the display
screen_width, screen_height = 1200, 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mystic Quest: Earth Mode")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 30)

# Load images for cutscene
hero = pygame.image.load('sun.png')
villain = pygame.image.load('zha_wujiang.png')

# Scale cutscene images
hero = pygame.transform.scale(hero, (400, 400))
villain = pygame.transform.scale(villain, (400, 400))

# Character positions for cutscene
hero_pos = (100, 350)
villain_pos = (700, 350)

# Dialogue texts for cutscene
hero_dialogues = [
    "I've been looking for you, zhu_bajie!",
    "Your reign of terror ends now.",
    "I'm not afraid of you!",
    "Prepare yourself!",
    "Send my luck to your boss."
]

villain_dialogues = [
    "Ha! You think you can stop me?",
    "This world belongs to us!",
    "You're just a nuisance.",
    "Let's see what you've got!"
]

# Load background video
background_video_path = 'golden.mp4'
background_video = mp.VideoFileClip(background_video_path)

# Load sounds
stone_collect_sound = pygame.mixer.Sound('collect_sound.wav')
dialogue_sound = pygame.mixer.Sound('warbgm.mp3')  # Sound for dialogue
pygame.mixer.music.load("warbgm.mp3")  # Load background music
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)

# Function to draw the background video frame
def draw_background(frame):
    frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
    frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))
    screen.blit(frame_surface, (0, 0))

# Function to draw speech bubbles
def draw_bubble(text, position, character_side, screen, font):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    bubble_padding = 20
    bubble_width = text_rect.width + bubble_padding * 2
    bubble_height = text_rect.height + bubble_padding * 2

    bubble_x = position[0] + 150 if character_side == "left" else position[0] - bubble_width + 250
    bubble_y = position[1] - 100

    pygame.draw.rect(screen, WHITE, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
    pygame.draw.rect(screen, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
    screen.blit(text_surface, (bubble_x + bubble_padding, bubble_y + bubble_padding))

# Function to display cutscene
def cutscene(dialogues, screen, font):
    clock = pygame.time.Clock()
    current_dialogue = 0
    total_dialogues = len(dialogues)
    
    running = True
    while running and current_dialogue < total_dialogues:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                if not pygame.mixer.get_busy():  # Check if any sound is currently playing
                    dialogue_sound.play()  # Play sound on dialogue
                current_dialogue += 1

        # Draw the background video frame
        current_time = (pygame.time.get_ticks() / 1000) % background_video.duration
        frame = background_video.get_frame(current_time)
        draw_background(frame)

        # Draw characters
        screen.blit(hero, hero_pos)
        screen.blit(villain, villain_pos)

        if current_dialogue < total_dialogues:
            character_name, dialogue = dialogues[current_dialogue]
            if character_name == "Hero":
                draw_bubble(dialogue, hero_pos, "left", screen, font)
            else:
                draw_bubble(dialogue, villain_pos, "right", screen, font)

        pygame.display.flip()
        clock.tick(30)

# Combine hero and villain dialogues
dialogues = list(zip(
    ["Hero", "Villain"] * min(len(hero_dialogues), len(villain_dialogues)),
    hero_dialogues + villain_dialogues
))

# Gameplay settings
player_width, player_height = 150, 150
player_images = [pygame.image.load(f"sun_moving_{i}.png").convert_alpha() for i in range(1, 10)]
player_images = [pygame.transform.scale(img, (player_width, player_height)) for img in player_images]

platform_image = pygame.transform.scale(pygame.image.load('tiles1.png'), (200, 80))
stone_image = pygame.transform.scale(pygame.image.load('stone_earth.png'), (60, 60))
background_image = pygame.transform.scale(pygame.image.load('moving_bg2.jpeg'), (screen_width, screen_height))

# Player settings
player_x, player_y = screen_width // 2, screen_height - 150
player_speed = 4
player_jump = False
jump_height = 20
gravity = 1
jump_velocity = 0
fall_speed = 15
ground_level = screen_height - player_height

platforms = [
    pygame.Rect(100, 500, 200, 20),
    pygame.Rect(400, 400, 200, 20),
    pygame.Rect(700, 300, 200, 20),
    pygame.Rect(1000, 200, 200, 20),
]

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
collected_stones = 0
start_time = time.time()
time_limit = 30

current_frame = 0
frame_delay = 5
frame_counter = 0

# Game state variables
cutscene_active = True  # Start with cutscene
game_over = False
win = False

# Main game loop
clock = pygame.time.Clock()
while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if cutscene_active:
        cutscene(dialogues, screen, font)  # Run cutscene
        cutscene_active = False  # End cutscene after it's done
        start_time = time.time()  # Reset timer for game
        pygame.mixer.music.play(-1)  # Start background music in a loop
    elif not game_over and not win:
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

        # Jumping and gravity mechanics
        if player_jump:
            player_y -= jump_velocity
            jump_velocity -= gravity
            if jump_velocity < 0:
                player_jump = False
        else:
            player_y += fall_speed

        # Handle platforms and stone collection
        for platform in platforms:
            platform.x -= 4
            if platform.right < 0:
                platform.x = screen_width
                stones = [s for s in stones if s['platform'] != platform]
                new_stones = generate_stones()
                stones.extend(new_stones)

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for stone in stones[:]:
            if player_rect.colliderect(stone['rect']):
                stones.remove(stone)
                collected_stones += 1
                stone_collect_sound.play()  # Play sound on collection
                if collected_stones >= total_stones:
                    win = True

        if elapsed_time >= time_limit:
            game_over = True

        # Draw everything
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

        font = pygame.font.SysFont(None, 36)
        collected_text = font.render(f"Collected Stones: {collected_stones}/{total_stones}", True, WHITE)
        screen.blit(collected_text, (screen_width - 300, 10))

        remaining_time = max(0, time_limit - int(elapsed_time))
        timer_text = font.render(f"Time Left: {remaining_time}", True, WHITE)
        screen.blit(timer_text, (screen_width - 300, 50))

        pygame.display.update()
        clock.tick(30)

    # Game Over or Win condition
    else:
        screen.fill(BLACK)
        if win:
            message = "You Win!"
        else:
            message = "Game Over"
        text_surface = font.render(message, True, WHITE)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    clock.tick(30)
