import pygame

pygame.init()

clock = pygame.time.Clock()

WIDTH = 1200
HEIGHT = 600 
BL_WIDTH = 200
BL_HEIGHT = 100
PLAYER_WIDTH = 330
PLAYER_HEIGHT = 220
PLAYER_VEL = 50
PLAYER_HEALTH = 100
SPELL_VEL = 10

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

BG = pygame.image.load("earth_bg.jpg").convert_alpha()
BG_img = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BL = pygame.image.load("bl.png").convert_alpha()
BL_img = pygame.transform.scale(BL, (BL_WIDTH, BL_HEIGHT))

sun = pygame.image.load("sun.png").convert_alpha()
sun_img = pygame.transform.scale(sun, (PLAYER_WIDTH, PLAYER_HEIGHT))

black_tortoise = pygame.image.load("black_tortoise.png").convert_alpha()
black_tortoise_img = pygame.transform.scale(black_tortoise, (PLAYER_WIDTH, PLAYER_HEIGHT))

earth_img = pygame.image.load("earth_atk.png").convert_alpha()
earth_spell = pygame.transform.scale(earth_img, (100, 100))

lightning_img = pygame.image.load("lightning_atk.png").convert_alpha()
lightning_spell = pygame.transform.scale(lightning_img, (100, 100))

def draw_IMG():
    
    WINDOW.blit(BG_img, (0, 0))
    WINDOW.blit(BL_img, (400, 0))

def draw(sun, black_tortoise, sun_health_rect, black_tortoise_health_rect, spells):
    WINDOW.blit(sun_img, (sun.x, sun.y))
    WINDOW.blit(black_tortoise_img, (black_tortoise.x, black_tortoise.y))

    for spell in spells:
        if spell["type"] == "lightning":
            WINDOW.blit(lightning_spell, (spell["rect"].x, spell["rect"].y))
        if spell["type"] == "earth":
            WINDOW.blit(earth_spell, (spell["rect"].x, spell["rect"].y))

    pygame.draw.rect(WINDOW, "green", sun_health_rect)
    pygame.draw.rect(WINDOW, "red", black_tortoise_health_rect)

def main():
    run = True

    sun = pygame.Rect(50, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    black_tortoise = pygame.Rect(WIDTH - PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    sun_health = PLAYER_HEALTH
    black_tortoise_health = PLAYER_HEALTH
    sun_health_rect = pygame.Rect(10, 10, sun_health * 3, 40)
    black_tortoise_health_rect = pygame.Rect(WIDTH - 300 - 10, 10, 300, 40)

    spells = []
    last_lightning_spell_time = pygame.time.get_ticks()
    last_earth_spell_time = pygame.time.get_ticks() 

    while run:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and sun.x - PLAYER_VEL >= 0:
            sun.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and sun.x + PLAYER_VEL + sun.width <= WIDTH:
            sun.x += PLAYER_VEL

        if keys[pygame.K_SPACE] and current_time - last_lightning_spell_time > 500:
            lightning_spell_rect = pygame.Rect(sun.x + sun.width, sun.y + sun.height // 2 - 50, 100, 100)
            spells.append({"type": "lightning", "rect": lightning_spell_rect})
            last_lightning_spell_time = current_time

        if current_time - last_earth_spell_time >= 2000:
            earth_spell_rect = pygame.Rect(black_tortoise.x, black_tortoise.y + black_tortoise.height // 2 - 50, 100, 100)
            spells.append({"type": "earth", "rect": earth_spell_rect})
            last_earth_spell_time = current_time

        for spell in spells[:]:
            if spell["type"] == "lightning":
                spell["rect"].x += SPELL_VEL
                if spell["rect"].colliderect(black_tortoise):
                    black_tortoise_health -= 10
                    black_tortoise_health_rect.width = black_tortoise_health * 3
                    spells.remove(spell)
                elif spell["rect"].x > WIDTH:
                    spells.remove(spell)

            elif spell["type"] == "earth":
                spell["rect"].x -= SPELL_VEL
                if spell["rect"].colliderect(sun):
                    sun_health -= 10
                    sun_health_rect.width = sun_health * 3
                    spells.remove(spell)
                elif spell["rect"].x < 0:
                    spells.remove(spell)

        for spell in spells[:]:
            for other_spell in spells[:]:
                if spell != other_spell and spell["rect"].colliderect(other_spell["rect"]):
                    if (spell["type"] == "lightning" and other_spell["type"] == "earth") or \
                            (spell["type"] == "earth" and other_spell["type"] == "lightning"):
                        spells.remove(spell)
                        spells.remove(other_spell)

        draw_IMG()    
        draw(sun, black_tortoise, sun_health_rect, black_tortoise_health_rect, spells)

        pygame.display.update()

        if sun_health <= 0:
            print("Game Over! Player has been defeated.")
            run = False
        elif black_tortoise_health <= 0:
            print("Congratulations! You have completed the first level.")  
            run = True

        clock.tick(60) 

    pygame.quit()

main()
