import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1200, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MYSTIC QUEST")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 50)

# Load images
background_image = pygame.image.load('cs.png')  # Load the background image
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale to fit the screen

stage_images = [
    pygame.image.load('stonestage.png'),  # Load Stage 1 image
    pygame.image.load('windstage.png'),   # Load Stage 2 image
    pygame.image.load('waterstage.png'),  # Load Stage 3 image
    pygame.image.load('firestage.png')    # Load Stage 4 image
]

# Load and scale the padlock image for locked stages
padlock_image = pygame.image.load('padlock.png')  # Load the padlock image
padlock_image = pygame.transform.scale(padlock_image, (50, 50))  # Scale the padlock image

# Scale stage images appropriately
stage_images = [pygame.transform.scale(img, (200, 200)) for img in stage_images]

# Stage button positions
stage_positions = [
    (200, 200),  # Position for Stage 1
    (800, 200),  # Position for Stage 2
    (200, 450),  # Position for Stage 3
    (800, 450)   # Position for Stage 4
]

# Stage names
stage_names = ["Underworld", "Sky Vale", "Aqua Palace", "Devils Lair"]

# Stage tracker
current_stage = "start"  # Possible values: "start", 0, 1, 2, 3 (index of stages)
unlocked_stages = 1  # Initially only Stage 1 is unlocked

# Time variable for animation
animation_time = 0

# Function to create a floating effect using sine wave
def get_floating_position(base_position, time_offset):
    """Get the new Y position based on the floating effect."""
    x, base_y = base_position
    float_range = 15  # Vertical floating range (in pixels)
    speed = 0.005  # Speed of the floating effect

    # Use sine wave for smooth floating motion
    new_y = base_y + math.sin(animation_time * speed + time_offset) * float_range
    return (x, int(new_y))

# Draw text function
def draw_text(text, position):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)

# Draw stage function with floating effect
def draw_stage(image, base_position, name, locked=False, time_offset=0):
    # Get the new floating position based on time
    position = get_floating_position(base_position, time_offset)
    
    # Draw the stage image at the new floating position
    screen.blit(image, position)

    # Title Position 
    name_position = (position[0] + 30, position[1] + 210)  # Adjust name position to float with the stage
    draw_text(name, name_position)

    # If the stage is locked, draw the padlock image
    if locked:
        padlock_position = (position[0] + 75, position[1] + 75)
        screen.blit(padlock_image, padlock_position)

# Main game loop
def maps_main():
    global animation_time, current_stage, unlocked_stages

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
                            current_stage = i
                            if current_stage == 0:
                                from Platform_1 import platform_1_main
                                platform_1_main()
                            elif current_stage == 1:
                                from Platform2 import platform_2_main
                                platform_2_main()
                            elif current_stage == 2:
                                from Platform_3 import platform_3_main
                                platform_3_main()
                            elif current_stage == 3:
                                from Platform4 import platform_4_main
                                platform_4_main()
                elif current_stage < len(stage_images):
                    # Simulate completing a stage by pressing any mouse button
                    current_stage = "start"
                    unlocked_stages = min(unlocked_stages + 1, 4)  # Unlock the next stage

        # Draw the screen based on the current stage
        if current_stage == "start":
            # Draw the background
            screen.blit(background_image, (0, 0))

            # Draw each stage (planet) with names and locked overlay, and apply the floating effect
            for i, (image, position, name) in enumerate(zip(stage_images, stage_positions, stage_names)):
                draw_stage(image, position, name, locked=i >= unlocked_stages, time_offset=i * 2)

            # Draw the "Select a Stage" text
            draw_text("Select a Stage", (500, 100))

        else:
            # Display the selected stage content
            screen.blit(stage_images[current_stage], (500, 250))  # Center the stage image on screen
            draw_text(stage_names[current_stage], (550, 50))  # Display stage name at the top

        # Update the display
        pygame.display.flip()

        # Floating Speed
        animation_time += clock.tick(15)  # TIKTIK

if __name__ == "__main__":
        maps_main()