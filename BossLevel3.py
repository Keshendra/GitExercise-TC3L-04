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
SPELL_VEL = 10

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

BG = pygame.image.load("water_bg.jpg").convert_alpha()
BG_img = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BL = pygame.image.load("bl.png").convert_alpha()
BL_img = pygame.transform.scale(BL, (BL_WIDTH, BL_HEIGHT))

hero = pygame.image.load("Hero.png").convert_alpha()
hero_img = pygame.transform.scale(hero, (PLAYER_WIDTH, PLAYER_HEIGHT))

enemy3 = pygame.image.load("water.png").convert_alpha()
enemy3_img = pygame.transform.scale(enemy3, (PLAYER_WIDTH, PLAYER_HEIGHT))

water_img = pygame.image.load("water_atk.png").convert_alpha()
water_spell = pygame.transform.scale(water_img, (100, 100))

lightning_img = pygame.image.load("lightning_atk.png").convert_alpha()
lightning_spell = pygame.transform.scale(lightning_img, (100, 100))

def draw_IMG():

    WINDOW.blit(BG_img, (0, 0))
    WINDOW.blit(BL_img, (400, 0))

def draw(hero, enemy3, hero_health_rect, enemy3_health_rect, spells):
    
    WINDOW.blit(hero_img, (hero.x, hero.y))
    WINDOW.blit(enemy3_img, (enemy3.x, enemy3.y))

    for spell in spells:
        if spell["type"] == "lightning":
            WINDOW.blit(lightning_spell, (spell["rect"].x, spell["rect"].y))
        if spell["type"] == "water":
            WINDOW.blit(water_spell, (spell["rect"].x, spell["rect"].y))
        
    pygame.draw.rect(WINDOW, "green", hero_health_rect)
    pygame.draw.rect(WINDOW, "red", enemy3_health_rect)


def main():
    run = True

    hero = pygame.Rect(50, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemy3 = pygame.Rect(WIDTH - PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    hero_health = PLAYER_HEALTH
    enemy3_health = PLAYER_HEALTH
    hero_health_rect = pygame.Rect(10, 10, hero_health * 3, 40)
    enemy3_health_rect = pygame.Rect(WIDTH - 300 - 10, 10, 300, 40)

    spells = []
    last_lightning_spell_time = pygame.time.get_ticks()
    last_water_spell_time = pygame.time.get_ticks() 


    while run:
        current_time = pygame.time.get_ticks()

        if current_time - last_water_spell_time >= 3000:
            water_spell_rect = pygame.Rect(enemy3.x, enemy3.y + enemy3.height // 2 - 50, 100, 100)
            spells.append({"type": "water", "rect": water_spell_rect})
            last_water_spell_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and hero.x - PLAYER_VEL >= 0:
                hero.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and hero.x + PLAYER_VEL + hero.width <= WIDTH:
                hero.x += PLAYER_VEL
            if keys[pygame.K_SPACE] and current_time - last_lightning_spell_time:
                lightning_spell_rect = pygame.Rect(hero.x + hero.width, hero.y + hero.height // 2 - 50, 100, 100)
                spells.append({"type": "lightning", "rect": lightning_spell_rect})
                last_lightning_spell_time = current_time
                
            for spell in spells[:]:
                if spell["type"] == "lightning":
                    spell["rect"].x += SPELL_VEL
                    if spell["type"] == "lightning" and spell["rect"].colliderect(enemy3):
                        enemy3_health -= 10
                        enemy3_health_rect.width = enemy3_health * 3
                        spells.remove(spell)

                elif spell["type"] == "water":
                    spell["rect"].x -= SPELL_VEL
                    if spell["type"] == "water" and spell["rect"].colliderect(hero):
                        hero_health -= 10
                        hero_health_rect.width = hero_health * 3
                        spells.remove(spell)           

                if spell["rect"].x < 0 or spell["rect"].y < 0 or spell["rect"].x > WIDTH or spell["rect"].y > HEIGHT:
                    spells.remove(spell)

        draw_IMG()    
        draw(hero, enemy3, hero_health_rect, enemy3_health_rect, spells)
        
        pygame.display.update()

        if hero_health <= 0:
            print("Game Over! Player has been defeated.")
            run = False
        elif enemy3_health <= 0:
            print("Congratulations! You have completed the first level.")  
            run = True


    pygame.quit()

main()