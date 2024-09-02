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
start_img = pygame.image.load("start_button.png").convert_alpha()
instruction_img = pygame.image.load("instruction.button.png").convert_alpha()
exit_img = pygame.image.load("exit.button.png").convert_alpha()
next_img = pygame.image.load("forward_button.png").convert_alpha()
back_img = pygame.image.load("backward_button.png").convert_alpha()

# Center calculation helper function
def center_position(image, screen_width, screen_height, offset_x=0, offset_y=0):
    x = (screen_width - image.get_width()) // 2 + offset_x
    y = (screen_height - image.get_height()) // 2 + offset_y
    return x, y

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

        # Reset clicked state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action 

# Create button instances with centered positions
button_x_start, button_y_start = center_position(start_img, WIDTH, HEIGHT, offset_y=-150)
start_button = Button(button_x_start, button_y_start, start_img)

button_x_instruction, button_y_instruction = center_position(instruction_img, WIDTH, HEIGHT)
instruction_button = Button(button_x_instruction, button_y_instruction, instruction_img)

button_x_exit, button_y_exit = center_position(exit_img, WIDTH, HEIGHT, offset_y=150)
exit_button = Button(button_x_exit, button_y_exit, exit_img)

forward_button = Button(900, 480, next_img, 1)  # Positioned the button for better visibility
backward_button = Button(100, 480, back_img, 1)  # Positioned the button for better visibility

# Set up the font
font = pygame.font.SysFont('Arial Black', 30)
text_color = (255, 255, 255)  # White color

# Pages content
pages = [
    ["There is a village named Songkaran Village,", "there was a farmer and while he was working he saw ", "an ancient treasure hidden", "deep within the paddy field."],
    ["The farmer went and took it from", "dark forests and across", "and touched it and got thrown far away, and he fainted", "once he woke up he was surrounded by village People."],
    ["Few months later he found out he has super power", "There were Elemental Guardians that escaped from the cave of GOD", "Village People were attacked by The Elemental Guardians such as", "FIRE, WATER, WIND, EARTH", "Then Hero showed up and fought against THEM."],
    ["DUN DUN DUN ", "TO BE CONTINUED,"]
]

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
STORY = 'story'
INSTRUCTIONS = 'instructions'
state = MENU

# Current Page
current_page = 0

# Function to display the text with a border
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
    
    # Draw the start button and check if it's clicked
    if start_button.draw(screen):
        return STORY
    
    # Draw the instruction button and check if it's clicked
    if instruction_button.draw(screen):
        return INSTRUCTIONS

    # Draw the exit button and check if it's clicked
    if exit_button.draw(screen):
        pygame.quit()
        sys.exit()

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

def draw_instructions_page():
    screen.fill((0, 0, 0))  # Fill the screen with black
    draw_text(screen, instructions, font, text_color)
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
        elif state == INSTRUCTIONS:
            draw_instructions_page()

    pygame.quit()

main()