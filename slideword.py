import pygame
import sys
import moviepy.editor as mp
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1200, 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mystic Quest")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 30)

# Load images
hero = pygame.image.load('sun.png')          # Hero image
villain = pygame.image.load('zha_wujiang.png')  # Villain image

# Scale images
hero = pygame.transform.scale(hero, (400, 400))
villain = pygame.transform.scale(villain, (400, 400))

# Character positions
hero_pos = (100, 350)       # Hero on the left side
villain_pos = (700, 350)    # Villain on the right side

# Dialogue texts
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

# Load the background video
background_video_path = 'golden.mp4'  # Ensure the path is correct
background_video = mp.VideoFileClip(background_video_path)

# Function to draw the background video frame
def draw_background(frame):
    frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
    frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))
    screen.blit(frame_surface, (0, 0))

# Function to draw speech bubbles
def draw_bubble(text, position, character_side, screen, font):
    # Render the text
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()

    # Set bubble dimensions and position
    bubble_padding = 20
    bubble_width = text_rect.width + bubble_padding * 2
    bubble_height = text_rect.height + bubble_padding * 2

    if character_side == "left":
        bubble_x = position[0] + 150  # Bubble appears to the right of the hero
    else:
        bubble_x = position[0] - bubble_width + 250  # Bubble appears to the left of the villain

    bubble_y = position[1] - 100  # Above the character

    # Draw the speech bubble rectangle
    pygame.draw.rect(screen, WHITE, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
    pygame.draw.rect(screen, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)

    # Blit the text inside the bubble
    screen.blit(text_surface, (bubble_x + bubble_padding, bubble_y + bubble_padding))

# Function to display cutscene with speech bubbles changing on key press
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
                current_dialogue += 1  # Go to the next dialogue

        # Draw the background video frame
        current_time = (pygame.time.get_ticks() / 1000) % background_video.duration
        frame = background_video.get_frame(current_time)
        draw_background(frame)

        # Draw characters
        screen.blit(hero, hero_pos)       # Hero
        screen.blit(villain, villain_pos) # Villain

        # Check if there are dialogues left to display
        if current_dialogue < total_dialogues:
            character_name, dialogue = dialogues[current_dialogue]
            if character_name == "Hero":
                draw_bubble(dialogue, hero_pos, "left", screen, font)
            else:
                draw_bubble(dialogue, villain_pos, "right", screen, font)

        pygame.display.flip()
        clock.tick(30)

# Combine hero and villain dialogues in order for cutscene
dialogues = list(zip(
    ["Hero", "Villain"] * min(len(hero_dialogues), len(villain_dialogues)),
    hero_dialogues + villain_dialogues
))

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # Check for "D" key press to start the dialogue sequence
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            cutscene(dialogues, screen, font)  # Start the dialogue sequence

    # Draw the background video frame
    current_time = (pygame.time.get_ticks() / 1000) % background_video.duration
    frame = background_video.get_frame(current_time)
    draw_background(frame)

    # Draw characters
    screen.blit(hero, hero_pos)       # Hero
    screen.blit(villain, villain_pos) # Villain

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Cleanup
background_video.close()
pygame.quit()
sys.exit()
