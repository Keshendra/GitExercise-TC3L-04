import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for screen dimensions
WIDTH, HEIGHT = 1200, 750

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mystic Quest")

# Load and scale background images
BG_MENU = pygame.transform.scale(pygame.image.load("m.jpg"), (WIDTH, HEIGHT))
BG_INSTRUCTIONS = pygame.transform.scale(pygame.image.load("inst_wall.jpg"), (WIDTH, HEIGHT)) # Instructions background

# Load button image
instruction_img = pygame.image.load("instruction.button.png").convert_alpha()

# Button class
class Button:
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

# Create the instruction button instance
button_x = (WIDTH - instruction_img.get_width()) // 2
button_y = (HEIGHT - instruction_img.get_height()) // 2
instruction_button = Button(button_x, button_y, instruction_img)

# Set up the font
font = pygame.font.SysFont('Arial Black', 30)
text_color = (255, 255, 255)  # White color

# Instructions content
instructions = [
    "Welcome to the instructions page!",
    "This game is all about exploring and adventuring.",
    "Use the arrow keys to navigate.",
    "Press the spacebar to interact with objects.",
    "Enjoy your journey and good luck!"
]

# Game States
MENU = 'menu'
INSTRUCTIONS = 'instructions'
state = MENU

# Function to display the instructions text
def draw_text(screen, text, font, color):
    y_position = 150
    for line in text:
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(line_surface, line_rect)
        y_position += 50

def draw_main_menu():
    screen.blit(BG_MENU, (0, 0))
    
    # Draw the instruction button and check if it's clicked
    if instruction_button.draw(screen):
        return INSTRUCTIONS

    pygame.display.flip()
    return MENU

def draw_instructions_page():
    screen.blit(BG_INSTRUCTIONS, (0, 0))  # Display the instructions background
    draw_text(screen, instructions, font, text_color)
    pygame.display.flip()
    return INSTRUCTIONS

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
        elif state == INSTRUCTIONS:
            state = draw_instructions_page()

    pygame.quit()

main()
