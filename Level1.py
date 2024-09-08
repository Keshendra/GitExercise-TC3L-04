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
hero = pygame.image.load('sun.png')            # Hero image
villain = pygame.image.load('black_tortoise.png')     # Villain image, ensure path is correct

# Scale images
background = pygame.transform.scale(background, (screen_width, screen_height))
hero = pygame.transform.scale(hero, (400, 400))
villain = pygame.transform.scale(villain, (400, 400))

# Character positions
hero_pos = (100, 350)       # Hero on the left side
villain_pos = (700, 350)    # Villain on the right side

# Dialogue bubble settings
bubble_width = 300
hero_bubble_pos = (hero_pos[0] + 150, hero_pos[1] - 70)
villain_bubble_pos = (villain_pos[0] - 50, villain_pos[1] - 70)

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

# Counters for dialogues
hero_counter = 0
villain_counter = 0
dialogue_state = "hero"  # Possible states: hero, villain, fight

# Function to wrap text
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

# Draw dialogue bubble function
def draw_dialogue_bubble(position, text):
    wrapped_text = wrap_text(text, font, bubble_width - 20)
    line_height = 20
    bubble_height = 10 + len(wrapped_text) * line_height + 10
    
    pygame.draw.rect(screen, WHITE, (position[0], position[1], bubble_width, bubble_height))
    pygame.draw.polygon(screen, WHITE, [(position[0] + 20, position[1] + bubble_height), 
                                        (position[0] + 40, position[1] + bubble_height), 
                                        (position[0] + 30, position[1] + bubble_height + 20)])
    pygame.draw.rect(screen, BLACK, (position[0], position[1], bubble_width, bubble_height), 2)
    
    for i, line in enumerate(wrapped_text):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (position[0] + 10, position[1] + 10 + i * line_height))

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for "D" key press to switch dialogues or start fight
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            if dialogue_state == "hero":
                hero_counter = (hero_counter + 1) % len(hero_dialogues)
                if hero_counter == 0:
                    dialogue_state = "villain"  # Move to villain dialogue
            elif dialogue_state == "villain":
                villain_counter = (villain_counter + 1) % len(villain_dialogues)
                if villain_counter == 0:
                    dialogue_state = "fight"  # Move to fight scene

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw characters
    screen.blit(hero, hero_pos)       # Hero
    screen.blit(villain, villain_pos) # Villain

    # Draw dialogue bubbles
    if dialogue_state == "hero":
        draw_dialogue_bubble(hero_bubble_pos, hero_dialogues[hero_counter])
    elif dialogue_state == "villain":
        draw_dialogue_bubble(villain_bubble_pos, villain_dialogues[villain_counter])
    elif dialogue_state == "fight":
        # Implement fight mechanics here
        draw_dialogue_bubble(hero_bubble_pos, "The fight begins!")
        draw_dialogue_bubble(villain_bubble_pos, "You don't stand a chance!")

    # Update the display
    pygame.display.flip()
    clock.tick(30)
