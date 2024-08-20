import pygame

pygame.init()

WIDTH = 1200
HEIGHT = 780

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

BG = pygame.image.load("bg_img.jpg")

def draw():
    WINDOW.blit(BG, (0, 0))
    pygame.display.update()

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        draw() 
        pygame.display.flip()

    pygame.quit()

main()