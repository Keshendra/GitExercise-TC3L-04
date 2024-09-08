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
background = pygame.image.load('scenery.jpg')  # Ensure the path is correct
villagers = pygame.image.load('village.png')   # Ensure the path is correct
hero = pygame.image.load('sun.png')           # Ensure the path is correct

# Scale images
background = pygame.transform.scale(background, (screen_width, screen_height))
villagers = pygame.transform.scale(villagers, (500, 400))
hero = pygame.transform.scale(hero, (300, 400))

# Character positions (lowered by increasing the y-coordinates)
villagers_pos = (50, 350)  # Lowered villagers by 100 pixels
hero_pos = (700, 350)      # Lowered hero by 100 pixels

# Dialogue bubble settings
bubble_width, bubble_height = 300, 100
villager_bubble_pos = (villagers_pos[0] + 100, villagers_pos[1] - bubble_height - 10)
hero_bubble_pos = (hero_pos[0] + 150, hero_pos[1] - bubble_height - 20)

# Dialogue texts
villager_dialogues = ["Hello, Rocky!", "Can you help us?", "We need your skills!", "Please save our village!"]
hero_dialogues = ["Heyy, What did you guys gather here?", "What is the problem?", "I am here to help.", "Let's save the day!"]

# Counters for dialogues
villager_counter = 0
hero_counter = 0
villager_turn = True

# Function to wrap text
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        # Check if adding the next word would exceed the max width
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            # Add the current line to the lines list and reset the current line
            lines.append(current_line)
            current_line = word
    
    # Add the last line
    if current_line:
        lines.append(current_line)
    
    return lines

# Draw dialogue bubble function
def draw_dialogue_bubble(position, text):
    pygame.draw.rect(screen, WHITE, (position[0], position[1], bubble_width, bubble_height))
    pygame.draw.polygon(screen, WHITE, [(position[0] + 20, position[1] + bubble_height), 
                                        (position[0] + 40, position[1] + bubble_height), 
                                        (position[0] + 30, position[1] + bubble_height + 20)])
    pygame.draw.rect(screen, BLACK, (position[0], position[1], bubble_width, bubble_height), 2)

    # Wrap text to fit within the bubble
    wrapped_text = wrap_text(text, font, bubble_width - 20)
    
    # Render each line of the wrapped text
    for i, line in enumerate(wrapped_text):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (position[0] + 10, position[1] + 10 + i * 20))  # Adjust line height as needed

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for space bar press to switch dialogues
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Switch dialogue on space press
            if villager_turn:
                villager_counter = (villager_counter + 1) % len(villager_dialogues)
            else:
                hero_counter = (hero_counter + 1) % len(hero_dialogues)
            villager_turn = not villager_turn  # Toggle turn between villager and hero

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw characters
    screen.blit(villagers, villagers_pos)  # Villagers
    screen.blit(hero, hero_pos)  # Hero

    # Draw dialogue bubbles
    if villager_turn:
        draw_dialogue_bubble(villager_bubble_pos, villager_dialogues[villager_counter])
    else:
        draw_dialogue_bubble(hero_bubble_pos, hero_dialogues[hero_counter])

    # Update the display
    pygame.display.flip()
    clock.tick(30)
