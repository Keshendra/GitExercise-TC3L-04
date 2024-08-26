import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1200, 780
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MYSTIC QUEST")

# Load and scale the background images
backgrounds = [
    pygame.transform.scale(pygame.image.load('farm.jpg'), (width, height)),    # Background for page 1
    pygame.transform.scale(pygame.image.load('treasure.png'), (width, height)),  # Background for page 2
    pygame.transform.scale(pygame.image.load('element.jpeg'),(width,height)),   # Background for page 3
    pygame.transform.scale(pygame.image.load('TBC.jpeg'),(width,height))     # Background for page 4
]

# Load button images
next_img = pygame.image.load("forward_button.png")
back_img = pygame.image.load("backward_button.png")

# Simple Button class definition
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()  # Get mouse position

        if self.rect.collidepoint(pos):  # Check if mouse is over the button
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Create button instances
forward_button = Button(900, 480, next_img, 1)  # Positioned the button for better visibility
backward_button = Button(100, 480, back_img, 1)  # Positioned the button for better visibility

# Set up the font
font = pygame.font.SysFont('Arial Black', 30)
text_color = (255, 255, 255)  # White color

# Pages content
pages = [
    ["There is a village named Songkaran Village,", "there was a farmer and while he was working he saw ", "an ancient treasure hidden", "deep within the paddy field."],
    ["the farmer went and took it from", "dark forests and across", "and touch and he got thrown far away, and he fainted", "once he awake he was surronded by village People."],
    ["Few months later he found out he has super power", "The was Elemental Guardians that escaped from cave of GOD", "Village People was attacked by The Elemental Guardians such as","FIRE,WATER,WIND,EARTH","Then Hero showed up and fight against THEM ."],
    ["DUN DUN DUN ", "TO BE CONTINUED,"]  # New page
]

# Current Page
current_page = 0 

# Function to display the story text
def draw_text(screen, text, font, color):
    y_position = 150
    for line in text:
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect(center=(width // 2, y_position))
        screen.blit(line_surface, line_rect)
        y_position += 40

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the current background
    screen.blit(backgrounds[current_page], (0, 0))

    # Draw the current page's text
    draw_text(screen, pages[current_page], font, text_color)

    # Draw and check if the next button is pressed
    if forward_button.draw(screen):
        current_page += 1
        if current_page >= len(pages):  # Loop back to the first page
            current_page = 0

    # Draw and check if the backward button is pressed
    if backward_button.draw(screen):
        current_page -= 1
        if current_page < 0:  # Loop back to the last page
            current_page = len(pages) - 1

    # Update the display
    pygame.display.flip()

