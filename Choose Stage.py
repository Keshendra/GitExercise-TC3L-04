import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1200, 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Stage Selection")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 50)

# Load images
background_image = pygame.image.load('maps_bg.jpg')  # Load the background image
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale to fit the screen

stage_images = [
    pygame.image.load('firestage.png'),  # Load Stage 1 image
    pygame.image.load('waterstage.png'),  # Load Stage 2 image
    pygame.image.load('stonestage.png'),  # Load Stage 3 image
    pygame.image.load('windstage.png')       # Load Stage 4 image
]

# Load and scale the padlock image for locked stages
padlock_image = pygame.image.load('padlock.png')  # Load the padlock image
padlock_image = pygame.transform.scale(padlock_image, (50, 50))  # Scale the padlock image

# Scale stage images appropriately
stage_images = [pygame.transform.scale(img, (200, 200)) for img in stage_images]

# Stage button positions (adjusting lower positions to show names better)
stage_positions = [
    (200, 200),  # Position for Stage 1
    (800, 200),  # Position for Stage 2
    (200, 450),  # Position for Stage 3 (moved lower)
    (800, 450)   # Position for Stage 4 (moved lower)
]

# Stage names
stage_names = ["Devils Lair", "Aqua Lair", "Underworld", "SkyVale"]

# Stage tracker
current_stage = "start"  # Possible values: "start", 0, 1, 2, 3 (index of stages)
unlocked_stages = 1  # Initially only Stage 1 is unlocked

# Draw text function
def draw_text(text, position):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)

# Draw stage function
def draw_stage(image, position, name, locked=False):
    screen.blit(image, position)  # Draw the stage image
    name_position = (position[0] + 50, position[1] + 210)  # Position the name below the image
    draw_text(name, name_position)

    # If the stage is locked, draw the padlock image
    if locked:
        padlock_position = (position[0] + 75, position[1] + 75)  # Center the padlock on the stage image
        screen.blit(padlock_image, padlock_position)

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if current_stage == "start":
                # Check which stage button is clicked
                for i, position in enumerate(stage_positions):
                    stage_rect = pygame.Rect(position, (200, 200))
                    if stage_rect.collidepoint(mouse_pos) and i < unlocked_stages:
                        current_stage = i  # Go to the selected stage
            elif current_stage < len(stage_images):
                # Simulate completing a stage by pressing any mouse button
                current_stage = "start"
                unlocked_stages = min(unlocked_stages + 1, 4)  # Unlock the next stage

    # Draw the screen based on the current stage
    if current_stage == "start":
        # Draw the background
        screen.blit(background_image, (0, 0))
        # Draw each stage (planet) with names and locked overlay
        for i, (image, position, name) in enumerate(zip(stage_images, stage_positions, stage_names)):
            draw_stage(image, position, name, locked=i >= unlocked_stages)
        draw_text("Select a Stage", (500, 100))
    else:
        # Display the selected stage content
        screen.blit(stage_images[current_stage], (500, 250))  # Center the stage image on screen
        draw_text(stage_names[current_stage], (550, 50))  # Display stage name at the top

    # Update the display
    pygame.display.flip()
    clock.tick(30)
