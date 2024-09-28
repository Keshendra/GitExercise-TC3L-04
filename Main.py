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

# Define file paths
main_menu_video_path = "wall.mp4"  # Path to main menu video
button_images = ["play_button.png", "forward_button.png", "backward_button.png"]
music_path = "warbgm.mp3"  # Path to background music

# Define file paths for different background videos for each story page
story_video_paths = ["foggy.mp4", "snowy.mp4", "sakura.mp4", "fall.mp4"]

# Function to check if a file exists
def check_file_exists(file_path):
    if os.path.isfile(file_path):
        print(f"File found: {file_path}")
        return True
    else:
        print(f"Error: The file '{file_path}' does not exist.")
        return False

# Check if main menu video exists
if not check_file_exists(main_menu_video_path):
    pygame.quit()
    sys.exit()

# Check if button images exist
for button_image in button_images:
    if not check_file_exists(button_image):
        pygame.quit()
        sys.exit()

# Check if all story video files exist
if not all([check_file_exists(video) for video in story_video_paths]):
    pygame.quit()
    sys.exit()

# Load the background music
if check_file_exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.5)  # Set the volume
    pygame.mixer.music.play(-1)  # Play infinitely

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Story Of Sun")

# Load video for the main menu
try:
    main_menu_video = mp.VideoFileClip(main_menu_video_path)
    print("Main menu video loaded successfully.")
except OSError as e:
    print(f"Error: Could not load main menu video file. {e}")
    pygame.quit()
    sys.exit()

# Load videos for each story page background
story_videos = []
for video_path in story_video_paths:
    try:
        video = mp.VideoFileClip(video_path)
        story_videos.append(video)
        print(f"Loaded video: {video_path}")
    except OSError as e:
        print(f"Error: Could not load story video file '{video_path}'. {e}")
        pygame.quit()
        sys.exit()

# Load button images
try:
    start_img = pygame.image.load(button_images[0]).convert_alpha()
    next_img = pygame.image.load(button_images[1]).convert_alpha()
    back_img = pygame.image.load(button_images[2]).convert_alpha()
    print("Button images loaded successfully.")
except pygame.error as e:
    print(f"Error: Could not load button images. {e}")
    pygame.quit()
    sys.exit()

# Button class
class Button():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                print("Button clicked!")

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Create button instances
button_x = (WIDTH - start_img.get_width()) // 2
button_y = (HEIGHT - start_img.get_height()) // 2 + 100
start_button = Button(button_x, button_y, start_img)

forward_button = Button(900, 480, next_img, 0.75)
backward_button = Button(100, 480, back_img, 0.75)

# Set up the font
font = pygame.font.SysFont('Copperplate Gothic Bold Black', 36)
text_color = (255, 255, 255)  # White color
highlight_color = (0, 0, 0, 128)  # Transparent black highlight

# Story content split into pages
story_pages = [
    [
        "In a world bound by the balance of fire, water, air, and earth,",
        "a hero named Sun emerged. The harmony of these elements",
        "was at risk, with natural disasters wreaking havoc across the land.",
        "Volcanoes erupted fiercely, floods overwhelmed the villages,",
        "violent storms raged, and the earth shook uncontrollably.",
        "Sun, a boy newly born, came to conquer the village",
        "from the power of these four elements."
    ],
    [
        "Sun's first challenge was in the fiery realm of the Devil's Lair,",
        "a beast that scorched everything in its path. Armed with a shield",
        "forged in the heart of the sun, Sun battled the Red Bird,",
        "absorbing its flames and extinguishing its rage, restoring",
        "calm to the land of fire."
    ],
    [
        "Next, Sun ventured to the Temple of Tides, where the Water Guardian,",
        "a Blue Dragon, unleashed torrential waves. Using ancient songs",
        "that resonated with the water's rhythm, Sun soothed the Blue Dragon,",
        "calming the raging seas and bringing peace back to the waters."
    ],
    [
        "Continuing his journey, Sun faced the White Tiger in the skies",
        "and the mighty Black Tortoise in the Stone Fortress. With the Cloak of Calm,",
        "he tamed the winds, turning storms into gentle breezes, and by harnessing",
        "the power of the elements he had mastered, he defeated the Black Tortoise,",
        "stabilizing the quakes. Having restored balance, Sun returned as the hero",
        "who united the elements, his legend enduring through time."
    ]
]

# Game States
MENU = 'menu'
STORY = 'story'
state = MENU

# Current Page
current_page = 0

# Function to draw text with typewriter effect
def draw_highlighted_text(screen, text, font, color, highlight_color, max_width=1000, typing_speed=50):
    global start_time
    elapsed_time = (pygame.time.get_ticks() - start_time) // typing_speed  # Control typing speed
    total_characters = sum([len(line) for line in text])

    y_position = 150
    displayed_characters = 0
    lines = []

    for line in text:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)

    # Draw highlight and typewriter text line by line
    for line in lines:
        if displayed_characters >= elapsed_time:
            break

        # Limit characters per line according to the elapsed time
        line_to_display = line[:max(0, elapsed_time - displayed_characters)]
        line_surface = font.render(line_to_display, True, color)
        line_rect = line_surface.get_rect(center=(WIDTH // 2, y_position))

        # Highlight background
        highlight_rect = pygame.Rect(line_rect.x - 10, line_rect.y - 5, line_rect.width + 20, line_rect.height + 10)
        highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        highlight_surface.fill(highlight_color)

        # Draw the highlight and the text
        screen.blit(highlight_surface, highlight_rect.topleft)
        screen.blit(line_surface, line_rect)

        y_position += font.get_linesize() + 10
        displayed_characters += len(line)

# Function to display the main menu
def draw_main_menu():
    global start_time

    current_time = (pygame.time.get_ticks() - start_time) / 1000
    if current_time >= main_menu_video.duration:
        start_time = pygame.time.get_ticks()
        current_time = 0

    try:
        frame = main_menu_video.get_frame(current_time)
        frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
        frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
        screen.blit(frame_surface, (0, 0))
    except Exception as e:
        print(f"Error: Failed to display main menu video frame. {e}")

    # Draw the start button
    if start_button.draw(screen):
        global state
        state = STORY
        start_time = pygame.time.get_ticks()

# Function to display the story page with the appropriate video background
def draw_story_page():
    global current_page, start_time

    # Get the current story video
    story_video = story_videos[current_page]

    current_time = (pygame.time.get_ticks() - start_time) / 1000
    if current_time >= story_video.duration:
        start_time = pygame.time.get_ticks()
        current_time = 0

    try:
        frame = story_video.get_frame(current_time)
        frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
        frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
        screen.blit(frame_surface, (0, 0))
    except Exception as e:
        print(f"Error: Failed to display story video frame. {e}")

    # Draw the text with typewriter effect
    draw_highlighted_text(screen, story_pages[current_page], font, text_color, highlight_color)

    # Draw navigation buttons
    if forward_button.draw(screen) and current_page < len(story_pages) - 1:
        current_page += 1
        start_time = pygame.time.get_ticks()  # Reset start time for new page

    if backward_button.draw(screen) and current_page > 0:
        current_page -= 1
        start_time = pygame.time.get_ticks()  # Reset start time for new page

# Main game loop
start_time = pygame.time.get_ticks()  # Initialize start time
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the appropriate screen based on the game state
    if state == MENU:
        draw_main_menu()
    elif state == STORY:
        draw_story_page()

    # Update the display
    pygame.display.update()

# Clean up resources before quitting
main_menu_video.close()
for video in story_videos:
    video.close()

pygame.quit()
sys.exit()
