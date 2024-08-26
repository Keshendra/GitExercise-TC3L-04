import pygame

pygame.init()

clock = pygame.time.Clock()

WIDTH = 1000
HEIGHT = 500
BL_WIDTH = 200
BL_HEIGHT = 100
PLAYER_WIDTH = 330
PLAYER_HEIGHT = 220
PLAYER_VEL = 50
PLAYER_HEALTH = 100
SPELL_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

BG = pygame.image.load("earth_bg.jpg").convert_alpha()
BG_img = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BL = pygame.image.load("bl.png").convert_alpha()
BL_img = pygame.transform.scale(BL, (BL_WIDTH, BL_HEIGHT))

hero = pygame.image.load("Hero.png").convert_alpha()
hero_img = pygame.transform.scale(hero, (PLAYER_WIDTH, PLAYER_HEIGHT))

enermy = pygame.image.load("earth.png").convert_alpha()
enermy_img = pygame.transform.scale(enermy, (PLAYER_WIDTH, PLAYER_HEIGHT))

earth_img = pygame.image.load("earth_atk.png").convert_alpha()
earth_spell = pygame.transform.scale(earth_img, (100, 100))

lightning_img = pygame.image.load("lightning_atk.png").convert_alpha()
lightning_spell = pygame.transform.scale(lightning_img, (100, 100))

def draw_IMG():

    WINDOW.blit(BG_img, (0, 0))

    WINDOW.blit(BL_img, (400, 0))


def draw(hero, enermy, hero_health_rect, enermy_health_rect, spells):
    
    WINDOW.blit(hero_img, (hero.x, hero.y))
    WINDOW.blit(enermy_img, (enermy.x, enermy.y))

    for spell in spells:
        WINDOW.blit(earth_spell, (spell.x, spell.y))
        WINDOW.blit(lightning_spell, (spell.x, spell.y))

    pygame.draw.rect(WINDOW, "green", hero_health_rect)
  # pygame.draw.rect(WINDOW, "green", enermy_health_rect)

  # pygame.draw.rect(WINDOW, "red", hero_health_rect)
    pygame.draw.rect(WINDOW, "red", enermy_health_rect)


def main():
    run = True

    hero = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    enermy = pygame.Rect(WIDTH - PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    hero_health = PLAYER_HEALTH
    enermy_health = PLAYER_HEALTH
    hero_health_rect = pygame.Rect(10, 10, hero_health * 3, 40)
    enermy_health_rect = pygame.Rect(WIDTH - 300 - 10, 10, 300, 40)

    spells = []
    last_spell_time = pygame.time.get_ticks()

    while run:

        current_time = pygame.time.get_ticks()
        if current_time - last_spell_time > 3000:
            lightning_spell_rect = pygame.Rect(hero.x + hero.width, hero.y + hero.height // 2 - 30, 60, 60)
            earth_spell_rect = pygame.Rect(enermy.x - 60, enermy.y + enermy.height // 2 - 30, 60, 60)
            spells.append(lightning_spell_rect)
            spells.append(earth_spell_rect)
            last_spell_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and hero.x - PLAYER_VEL >= 0:
                hero.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and hero.x + PLAYER_VEL + hero.width <= WIDTH:
                hero.x += PLAYER_VEL
                
            for spell in spells[:]:
                direction_x = hero.x - spell.x
                direction_y = hero.y - spell.y

                distance = (direction_x**2 + direction_y**2)**0.5
                if distance != 0:
                    direction_x /= distance
                    direction_y /= distance
                
                spell.x += direction_x * SPELL_VEL
                spell.y += direction_y * SPELL_VEL

                if spell.colliderect(hero):
                    spells.remove(spell)
                    hero_health -= 10
                    hero_health_rect.width = hero_health * 3

                elif spell.x < 0 or spell.y < 0 or spell.x > WIDTH or spell.y > HEIGHT:
                    spells.remove(spell)

        draw_IMG()    
        draw(hero, enermy, hero_health_rect, enermy_health_rect, spells)
        
        pygame.display.update()

        if hero_health <= 0:
            print("Game Over! Player A has been defeated.")
            run = False


    pygame.quit()

main()