import pygame
import moviepy.editor as mp
import numpy as np
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants for screen dimensions
WIDTH, HEIGHT = 1200, 780
TYPE_SPEED = 50  # milliseconds per character

# Define file paths
main_menu_video_path = "wall.mp4"
button_images = ["play_button.png", "forward_button.png", "backward_button.png"]
music_path = "warbgm.mp3"
story_video_paths = ["foggy.mp4", "snowy.mp4", "sakura.mp4", "fall.mp4"]

# Check if a file exists
def check_file_exists(file_path):
    return os.path.isfile(file_path)

# Load files
if not check_file_exists(main_menu_video_path) or not all(check_file_exists(img) for img in button_images) or not all(check_file_exists(video) for video in story_video_paths):
    pygame.quit()
    sys.exit()

# Load background music
if check_file_exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Story Of Lumir")

# Load videos
main_menu_video = mp.VideoFileClip(main_menu_video_path)
story_videos = [mp.VideoFileClip(video) for video in story_video_paths]

# Load button images
start_img = pygame.image.load(button_images[0]).convert_alpha()
next_img = pygame.image.load(button_images[1]).convert_alpha()
back_img = pygame.image.load(button_images[2]).convert_alpha()
background_image = pygame.image.load('cs.png')  # Load the background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) 

# Button class
class Button():
    def __init__(self, x, y, image, scale=1):
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, self.rect.topleft)
        return action

# Create button instances
start_button = Button((WIDTH - start_img.get_width()) // 2, (HEIGHT - start_img.get_height()) // 2 + 100, start_img)
forward_button = Button(900, 480, next_img, 0.75)
backward_button = Button(100, 480, back_img, 0.75)

# Complete Story Content
story_pages = [
    [
        "In a world bound by the balance of fire, water, air, and earth,",
        "a hero named Lumir emerged. The harmony of these elements",
        "was at risk, with natural disasters wreaking havoc across the land.",
        "Volcanoes erupted fiercely, floods overwhelmed the villages,",
        "violent storms raged, and the earth shook uncontrollably.",
        "Lumir, a boy newly born, came to conquer the village",
        "from the power of these four elements."
    ],
    [
        "Lumir's first challenge was in the fiery realm of the Pyro Serpent,",
        "a beast that scorched everything in its path. Armed with a shield",
        "forged in the heart of the sun, Lumir battled the serpent,",
        "absorbing its flames and extinguishing its rage, restoring",
        "calm to the land of fire."
    ],
    [
        "Next, Lumir ventured to the Temple of Tides, where the Water Guardian,",
        "a colossal Leviathan, unleashed torrential waves. Using ancient songs",
        "that resonated with the water's rhythm, Lumir soothed the Leviathan,",
        "calming the raging seas and bringing peace back to the waters."
    ],
    [
        "Continuing his journey, Lumir faced the Tempest Eagle in the skies",
        "and the mighty Earth Golem in the Stone Fortress. With the Cloak of Calm,",
        "he tamed the winds, turning storms into gentle breezes, and by harnessing",
        "the power of the elements he had mastered, he defeated the Earth Golem,",
        "stabilizing the quakes. Having restored balance, Lumir returned as the hero",
        "who united the elements, his legend enduring through time."
    ]
]

# Game States
MENU = 'menu'
STORY = 'story'
MAPS = 'maps'
state = MENU
current_page = 0
current_text_index = 0
last_time_updated = pygame.time.get_ticks()

# Draw main menu
def draw_main_menu():
    current_time = (pygame.time.get_ticks() / 1000) % main_menu_video.duration
    frame = main_menu_video.get_frame(current_time)
    frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
    frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
    screen.blit(frame_surface, (0, 0))
    if start_button.draw(screen):
        global state, current_page, current_text_index
        state = STORY
        current_page = 0
        current_text_index = 0  # Reset text index for new story

# Draw story page with typewriter effect
def draw_story_page():
    global current_page, current_text_index, last_time_updated

    story_video = story_videos[current_page]
    current_time = (pygame.time.get_ticks() / 1000) % story_video.duration
    frame = story_video.get_frame(current_time)
    frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
    frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
    screen.blit(frame_surface, (0, 0))

    # Update the typewriter effect
    if pygame.time.get_ticks() - last_time_updated > TYPE_SPEED:
        last_time_updated = pygame.time.get_ticks()
        if current_text_index < len(story_pages[current_page]):
            current_text_index += 1  # Show the next line of text

    # Create a surface for the narration background
    narration_surface = pygame.Surface((800, 300), pygame.SRCALPHA)
    narration_surface.fill((0, 0, 0, 180))  # Transparent black background

    # Position the narration surface in the center
    narration_rect = narration_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(narration_surface, narration_rect.topleft)

    # Draw the current text within the narration area
    font = pygame.font.Font(None, 36)  # Set font for text rendering
    for i in range(current_text_index):
        text_surface = font.render(story_pages[current_page][i], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(narration_rect.centerx, narration_rect.top + 20 + i * font.get_height()))
        screen.blit(text_surface, text_rect.topleft)

    if forward_button.draw(screen):
        if current_page < len(story_pages) - 1 and current_text_index >= len(story_pages[current_page]):
            current_page += 1
            current_text_index = 0  # Reset text index for new page
        elif current_page == len(story_pages) - 1 and current_text_index >= len(story_pages[current_page]):
            global state
            state = MAPS  # Transition to maps page

    if backward_button.draw(screen) and current_page > 0:
        current_page -= 1
        current_text_index = 0  # Reset text index for new page

# Maps Page Setup
stage_images = [pygame.image.load('firestage.png'), pygame.image.load('waterstage.png'), 
                pygame.image.load('stonestage.png'), pygame.image.load('windstage.png')]

# Ensure the stage images are scaled to appropriate size (optional scaling factor)
stage_images = [pygame.transform.scale(img, (300, 200)) for img in stage_images]
stage_positions = [(200, 200), (800, 200), (200, 450), (800, 450)]
stage_names = ["Devils Lair", "Aqua Lair", "Underworld", "SkyVale"]
unlocked_stages = 1
current_stage = "start"

stage_buttons = [Button(pos[0], pos[1], img, scale=1) for pos, img in zip(stage_positions, stage_images)]

# Function to draw maps page
def draw_maps_page():
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    for i, (stage_button, name) in enumerate(zip(stage_buttons, stage_names)):
        # Draw stage image button
        if stage_button.draw(screen) and i < unlocked_stages:
            global current_stage, state
            current_stage = name
            state = "first_level"

        if i >= unlocked_stages:
            padlock_image = pygame.image.load('padlock.png')
            padlock_image = pygame.transform.scale(padlock_image, (50, 50))
            screen.blit(padlock_image, (stage_positions[i][0] + 75, stage_positions[i][1] + 75))  # Position padlock    

    # Highlight text with border
    font = pygame.font.Font(None, 48)
    highlight_text = font.render("Select a Stage", True, (255, 255, 255))
    text_rect = highlight_text.get_rect(center=(WIDTH // 2, 50))

    # Draw a border around the text
    border_rect = text_rect.inflate(20, 10)  # Create a rectangle larger than the text for the border
    pygame.draw.rect(screen, (0, 0, 255), border_rect)  # Blue border
    screen.blit(highlight_text, text_rect)  # Draw the text on top

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if state == MENU:
        draw_main_menu()
    elif state == STORY:
        draw_story_page()
    elif state == MAPS:
        draw_maps_page()

    pygame.display.update()

pygame.quit()
sys.exit()
