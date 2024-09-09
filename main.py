import pygame

pygame.init()

WIDTH = 1200
HEIGHT = 750

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

BG = pygame.image.load("bg_img.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BG_GAME = pygame.image.load("img_2.png")
BG_GAME = pygame.transform.scale(BG_GAME, (WIDTH, HEIGHT))

# Load button images
start_img = pygame.image.load("play.png").convert_alpha()
quit_img = pygame.image.load("quit.png").convert_alpha()
left_img = pygame.image.load("left_button.png").convert_alpha()
right_img = pygame.image.load("right_button.png").convert_alpha()

# Button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action 

# Position buttons on screen
button_x = (WIDTH - start_img.get_width()) // 2
button_y = (HEIGHT - start_img.get_height()) // 2
start_button = Button(button_x, button_y, start_img)

quit_button_x = (WIDTH - quit_img.get_width()) // 2
quit_button_y = button_y + start_img.get_height() + 30
quit_button = Button(quit_button_x, quit_button_y, quit_img)

left_button = Button(20, HEIGHT // 2 - left_img.get_height() // 2, left_img)
right_button = Button(WIDTH - right_img.get_width() - 20, HEIGHT // 2 - right_img.get_height() // 2, right_img)

MENU = 'menu'
INSTRUCTIONS = 'instructions'
GAME = 'game'
state = MENU

# Define the instruction pages list
instruction_texts = [
    "Welcome to Mystic Quest!\n\nUse arrow keys to move your character.\nPress SPACE to jump.\nAvoid obstacles and collect coins.",
    "In the game:\n\n- Use the UP arrow to jump higher.\n- Use the DOWN arrow to crouch.\n- Collect special items for bonus points.",
    "Good luck!\n\nIf you have any issues, refer to the Help section in the main menu.\n\nClick right to start the game or left to go back to the main menu."
]
current_instruction = 0

# Font for instructions
font = pygame.font.Font(None, 36)

def draw_main_menu():
    WINDOW.blit(BG, (0, 0))
    if start_button.draw(WINDOW):
        return INSTRUCTIONS
    if quit_button.draw(WINDOW):
        pygame.quit()
        exit()
    pygame.display.flip()
    return MENU

def draw_instructions_page():
    WINDOW.blit(BG, (0, 0))  # You can set a background if needed
    # Render instruction text
    text_surface = font.render(instruction_texts[current_instruction], True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WINDOW.blit(text_surface, text_rect)

    # Draw navigation buttons
    left_button.draw(WINDOW)
    right_button.draw(WINDOW)
    pygame.display.flip()

def draw_game_screen():
    WINDOW.blit(BG_GAME, (0, 0))
    pygame.display.flip()

def main():
    global state, current_instruction
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        if state == MENU:
            state = draw_main_menu()
        elif state == INSTRUCTIONS:
            draw_instructions_page()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if left_button.rect.collidepoint(pos):
                            state = MENU
                            break
                        if right_button.rect.collidepoint(pos):
                            current_instruction = (current_instruction + 1) % len(instruction_texts)
                            state = INSTRUCTIONS
                            break
                if state == MENU:
                    break
        elif state == GAME:
            draw_game_screen()

    pygame.quit()

main()
