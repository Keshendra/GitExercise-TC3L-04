import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for screen dimensions
WIDTH, HEIGHT = 1200, 750

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

# Load and scale background images
BG_MENU = pygame.transform.scale(pygame.image.load("m.jpg"), (WIDTH, HEIGHT))
backgrounds = [
    pygame.transform.scale(pygame.image.load('farm.jpg'), (WIDTH, HEIGHT)),    # Background for page 1
    pygame.transform.scale(pygame.image.load('treasure.png'), (WIDTH, HEIGHT)),  # Background for page 2
    pygame.transform.scale(pygame.image.load('element.jpeg'), (WIDTH, HEIGHT)),   # Background for page 3
    pygame.transform.scale(pygame.image.load('TBC.jpeg'), (WIDTH, HEIGHT))     # Background for page 4
]

# Load button images
start_img = pygame.image.load("button.start.png").convert_alpha()
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
font = pygame.font.SysFont('Arial Black', 30)
text_color = (255, 255, 255)  # White color

# Pages content
pages = [
    ["There is a village named Songkaran Village,", "there was a farmer and while he was working he saw ", "an ancient treasure hidden", "deep within the paddy field."],
    ["the farmer went and took it from", "dark forests and across", "and touch and he got thrown far away, and he fainted", "once he awake he was surronded by village People."],
    ["Few months later he found out he has super power", "The was Elemental Guardians that escaped from cave of GOD", "Village People was attacked by The Elemental Guardians such as", "FIRE,WATER,WIND,EARTH", "Then Hero showed up and fight against THEM."],
    ["DUN DUN DUN ", "TO BE CONTINUED,"]
]

# Game States
MENU = 'menu'
STORY = 'story'
state = MENU

# Current Page
current_page = 0

# Function to display the story text
def draw_text(screen, text, font, color):
    y_position = 150
    for line in text:
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

    screen.blit(backgrounds[current_page], (0, 0))
    draw_text(screen, pages[current_page], font, text_color)

    if forward_button.draw(screen):
        current_page += 1
        if current_page >= len(pages):
            current_page = 0  # Loop back to the first page

    if backward_button.draw(screen):
        current_page -= 1
        if current_page < 0:
            current_page = len(pages) - 1  # Loop back to the last page

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
