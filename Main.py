import pygame
import sys

pygame.init()

WIDTH = 1200
HEIGHT = 750

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")
 
BG = pygame.image.load("m.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BG_GAME = pygame.image.load("m.jpg")
BG_GAME = pygame.transform.scale(BG_GAME, (WIDTH, HEIGHT))

# Load button images
start_img = pygame.image.load("button.start.png").convert_alpha()

# Button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
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
    
button_x = (WIDTH - start_img.get_width()) // 2
button_y = (HEIGHT - start_img.get_height()) // 2 + 100
start_button = Button(button_x, button_y, start_img)  # Fixed Button initialization

MENU = 'menu'
GAME = 'game'
state = MENU

def draw_main_menu():
    WINDOW.blit(BG, (0, 0))
    if start_button.draw(WINDOW):
        return GAME
    pygame.display.flip()
    return MENU

def draw_game_screen():
    WINDOW.blit(BG_GAME, (0, 0))
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
        elif state == GAME:
            draw_game_screen()

    pygame.quit()

main()
