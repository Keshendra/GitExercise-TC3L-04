import pygame
import sys

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
background = pygame.image.load('bkg1.jpeg')  # Ensure the path is correct
hero = pygame.image.load('sun.png')          # Hero image
villain = pygame.image.load('black_tortoise.png')  # Villain image, ensure path is correct

# Scale images
background = pygame.transform.scale(background, (screen_width, screen_height))
hero = pygame.transform.scale(hero, (400, 400))
villain = pygame.transform.scale(villain, (400, 400))

# Character positions
hero_pos = (100, 350)       # Hero on the left side
villain_pos = (700, 350)    # Villain on the right side

# Dialogue texts
hero_dialogues = [
    "I've been looking for you, villain!",
    "Your reign of terror ends now.",
    "I'm not afraid of you!",
    "Prepare yourself!"
]

villain_dialogues = [
    "Ha! You think you can stop me?",
    "This world belongs to me!",
    "You're just a nuisance.",
    "Let's see what you've got!"
]

# Function to display cutscene with character names
def cutscene(dialogues, screen, font, window_width, top_bar_height=150, delay=0.05):
    clock = pygame.time.Clock()

    # Loop through the dialogues list
    for character_name, dialogue in dialogues:
        text_displayed = ""
        running = True

        # Loop through each character in the dialogue to display it one by one
        for char in dialogue:
            text_displayed += char
            clock.tick(20)  # Control frame rate

            # Event handling to allow exiting the cutscene with 'D' key
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:  
                    running = False  # Exit on 'D' key

            # Drawing the text on the screen
            pygame.draw.rect(screen, 'black', (0, 0, window_width, top_bar_height))
            name_surface = font.render(f"{character_name}:", True, 'white')
            name_rect = name_surface.get_rect(topleft=(20, 20))
            screen.blit(name_surface, name_rect)

            text_surface = font.render(text_displayed, True, 'white')
            text_rect = text_surface.get_rect(center=(window_width // 2, top_bar_height // 2))
            screen.blit(text_surface, text_rect)

            pygame.display.flip()

            # Control delay between displaying characters
            clock.tick(int(1 / delay))

        # Wait for 'D' key to advance to the next dialogue
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:  
                    running = False  # Exit on 'D' key

            # Keep the text displayed while waiting for the user to exit
            pygame.draw.rect(screen, 'black', (0, 0, window_width, top_bar_height))
            screen.blit(name_surface, name_rect)
            text_surface = font.render(text_displayed, True, 'white')
            text_rect = text_surface.get_rect(center=(window_width // 2, top_bar_height // 2))
            screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(30)  # Maintain a reasonable frame rate

# Combine hero and villain dialogues in order for cutscene
dialogues = list(zip(["Hero", "Villain"] * (len(hero_dialogues)), hero_dialogues + villain_dialogues))

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for "D" key press to start the dialogue sequence
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            cutscene(dialogues, screen, font, screen_width)  # Show all dialogues

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw characters
    screen.blit(hero, hero_pos)       # Hero
    screen.blit(villain, villain_pos) # Villain

    # Update the display
    pygame.display.flip()
    clock.tick(30)
