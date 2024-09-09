import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for screen dimensions
WIDTH, HEIGHT = 1200, 780

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

# Load and scale background images
BG_MENU = pygame.transform.scale(pygame.image.load("mainpage.jpg"), (WIDTH, HEIGHT))
backgrounds = [
    pygame.transform.scale(pygame.image.load('story1.jpg'), (WIDTH, HEIGHT)),    # Background for page 1
    pygame.transform.scale(pygame.image.load('story2.jpg'), (WIDTH, HEIGHT)),  # Background for page 2
    pygame.transform.scale(pygame.image.load('story3.jpg'), (WIDTH, HEIGHT)),   # Background for page 3
    pygame.transform.scale(pygame.image.load('story4.jpg'), (WIDTH, HEIGHT))     # Background for page 4
]

# Load button images
start_img = pygame.image.load("play_button.png").convert_alpha()
next_img = pygame.image.load("forward_button.png").convert_alpha()
back_img = pygame.image.load("backward_button.png").convert_alpha()

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

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action 

# Create button instances
button_x = (WIDTH - start_img.get_width()) // 2
button_y = (HEIGHT - start_img.get_height()) // 2 + 100
start_button = Button(button_x, button_y, start_img)

forward_button = Button(900, 480, next_img, 1)  # Positioned the button for better visibility
backward_button = Button(100, 480, back_img, 1)  # Positioned the button for better visibility

# Set up the font
font = pygame.font.SysFont('Arial Black', 28)
text_color = (255, 255, 255)  # White color

# Story content split into pages
story_pages = [
    ["Long ago, in a world where the lines between mortals",
     "and immortals were thin, a legendary figure named Sun",
     "embarked on a perilous quest. His desire was not wealth,",
     "power, or glory — it was immortality."],
    
    ["But to achieve this divine state, he must first defeat the Four",
     "Guardian Beasts that ruled the elements of the earth: the fiery Red Bird,",
     "the swift and serpentine Blue Dragon, the ferocious and steadfast White Tiger,",
     "and the wise and indomitable Black Tortoise."],
    
    ["Each guardian ruled over a sacred realm, defending their elemental",
     "power: Fire, Water, Earth, and Air. Only by conquering these ancient",
     "protectors could Sun hope to unlock the secret of eternal life."],
    
    ["With his staff in hand and his spirit unbroken, Sun journeyed",
     "across treacherous lands, facing danger, deceit, and the",
     "unrelenting force of nature itself. But the guardians were more",
     "than mere beasts—they embodied the virtues of their elements,",
     "and only by understanding their strength could Sun hope to defeat them."]
]

# Game States
MENU = 'menu'
STORY = 'story'
state = MENU

# Current Page
current_page = 0

# Function to display the story text with a border
def draw_text(screen, text, font, color, border_color=(0, 0, 0)):
    y_position = 150
    border_offset = 2  # Offset for the border thickness
    
    for line in text:
        # Render the text multiple times around the original position to create a border
        for dx, dy in [(-border_offset, 0), (border_offset, 0), (0, -border_offset), (0, border_offset),
                       (-border_offset, -border_offset), (-border_offset, border_offset),
                       (border_offset, -border_offset), (border_offset, border_offset)]:
            border_surface = font.render(line, True, border_color)
            border_rect = border_surface.get_rect(center=(WIDTH // 2 + dx, y_position + dy))
            screen.blit(border_surface, border_rect)

        # Render the original text in the center
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(line_surface, line_rect)

        y_position += 40

def draw_main_menu():
    screen.blit(BG_MENU, (0, 0))
    if start_button.draw(screen):
        return STORY
    pygame.display.flip()
    return MENU

def draw_story_page():
    global current_page

    screen.blit(backgrounds[current_page % len(backgrounds)], (0, 0))
    draw_text(screen, story_pages[current_page], font, text_color)

    if forward_button.draw(screen):
        current_page += 1
        if current_page >= len(story_pages):
            current_page = 0  # Loop back to the first page

    if backward_button.draw(screen):
        current_page -= 1
        if current_page < 0:
            current_page = len(story_pages) - 1  # Loop back to the last page

    pygame.display.flip()

def main():
    global state
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        if state == MENU:
            state = draw_main_menu()
        elif state == STORY:
            draw_story_page()

    pygame.quit()

main()
