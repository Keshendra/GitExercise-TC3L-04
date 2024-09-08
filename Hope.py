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
    pygame.transform.scale(pygame.image.load('Vic PIC.webp'), (width, height)),    # Background for page 1
    pygame.transform.scale(pygame.image.load('treasure.png'), (width, height)),  # Background for page 2
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
border_color = (0, 0, 0)  # Black color for the border

# Pages content
pages = [
    [
        "After a fierce battle, the village finally tasted freedom.",
        "The four elemental villains were vanquished by brave heroes.",
        "Villagers celebrated under the bright sky, dancing with joy.",
        "Children ran around, enjoying the newfound peace and safety."
    ],
    [
        "Feasts were prepared with fresh harvest from the farms.",
        "Songs of victory echoed through the air, and bonfires lit the night.",
        "The elders shared tales of the battle and honored the fallen.",
        "The village vowed to stand strong, united against future threats."
    ]
]

# Current Page
current_page = 0 

# Function to display the story text with a border
def draw_text(screen, text, font, color, border_color):
    y_position = 150
    for line in text:
        line_surface = font.render(line, True, color)
        border_surface = font.render(line, True, border_color)

        # Create a border effect by drawing the text multiple times slightly offset
        for offset_x, offset_y in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            border_rect = border_surface.get_rect(center=(width // 2 + offset_x, y_position + offset_y))
            screen.blit(border_surface, border_rect)

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

    # Draw the current page's text with a border
    draw_text(screen, pages[current_page], font, text_color, border_color)

    # Draw and check if the next button is pressed
    if forward_button.draw(screen):
        current_page += 1
        if current_page >= len(pages):  # Loop back to the first page
            current_page = 0

    # Draw and check if the backward button is pressed (except on the first page)
    if current_page > 0 and backward_button.draw(screen):
        current_page -= 1
        if current_page < 0:  # Loop back to the last page
            current_page = len(pages) - 1

    # Update the display
    pygame.display.flip()
