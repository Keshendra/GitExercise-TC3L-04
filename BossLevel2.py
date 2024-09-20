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

BG = pygame.image.load("air_bg.jpg").convert_alpha()
BG_img = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BL = pygame.image.load("bl.png").convert_alpha()
BL_img = pygame.transform.scale(BL, (BL_WIDTH, BL_HEIGHT))

sun = pygame.image.load("sun.png").convert_alpha()
sun_img = pygame.transform.scale(sun, (PLAYER_WIDTH, PLAYER_HEIGHT))

white_tiger = pygame.image.load("white_tiger.png").convert_alpha()
white_tiger_img = pygame.transform.scale(white_tiger, (PLAYER_WIDTH, PLAYER_HEIGHT))

air_img = pygame.image.load("air_atk.png").convert_alpha()
air_spell = pygame.transform.scale(air_img, (200, 200))

sun_black_spell_img = pygame.image.load("sun_black_spell.png").convert_alpha()
sun_black_spell = pygame.transform.scale(sun_black_spell_img, (200, 200))

#fire_spell_frame = [pygame.image.load(f"fire_spell_frame_{i}.png").convert_alpha() for i in range(1, 9)]
#current_fire_frame = 0
#frame_delay = 1
#frame_count = 0

wind_explosive_frames = [pygame.image.load(f"wind_explosive_frame_{i}.png").convert_alpha() for i in range(1, 3)]
wind_explosive_active = False
wind_explosive_pos = None
wind_explosive_frame = 0

def draw_IMG():
    
    WINDOW.blit(BG_img, (0, 0))
    WINDOW.blit(BL_img, (400, 0))

def draw(sun, white_tiger, sun_health_rect, white_tiger_health_rect, spells):
    global current_fire_frame, frame_count, wind_explosive_active, wind_explosive_frame

    WINDOW.blit(sun_img, (sun.x, sun.y))
    WINDOW.blit(white_tiger_img, (white_tiger.x, white_tiger.y))

    for spell in spells:
        if spell["type"] == "sun_black_spell":
            WINDOW.blit(sun_black_spell, (spell["rect"].x, spell["rect"].y))
        elif spell["type"] == "air":
            WINDOW.blit(air_spell, (spell["rect"].x, spell["rect"].y))

        if wind_explosive_active and wind_explosive_pos:
            WINDOW.blit(wind_explosive_frames[wind_explosive_frame], wind_explosive_pos)
            wind_explosive_frame += 1
            if wind_explosive_frame >= len(wind_explosive_frames):
                wind_explosive_active = False
                wind_explosive_frame = 0   

    pygame.draw.rect(WINDOW, "green", sun_health_rect)
    pygame.draw.rect(WINDOW, "red", white_tiger_health_rect)

def main():
    global wind_explosive_active, wind_explosive_pos

    run = True

    sun = pygame.Rect(50, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    white_tiger = pygame.Rect(WIDTH - PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    sun_health = PLAYER_HEALTH
    white_tiger_health = PLAYER_HEALTH
    sun_health_rect = pygame.Rect(10, 10, sun_health * 3, 40)
    white_tiger_health_rect = pygame.Rect(WIDTH - 300 - 10, 10, 300, 40)

    spells = []
    last_sun_black_spell_spell_time = pygame.time.get_ticks()
    last_air_spell_time = pygame.time.get_ticks() 

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

        if keys[pygame.K_SPACE] and current_time - last_sun_black_spell_spell_time > 500:
            sun_black_spell_spell_rect = pygame.Rect(sun.x + sun.width, sun.y + sun.height // 2 - 50, 100, 100)
            spells.append({"type": "sun_black_spell", "rect": sun_black_spell_spell_rect})
            last_sun_black_spell_spell_time = current_time

        if current_time - last_air_spell_time >= 3000:
            air_spell_rect = pygame.Rect(white_tiger.x, white_tiger.y + white_tiger.height // 2 - 50, 100, 100)
            spells.append({"type": "air", "rect": air_spell_rect})
            last_air_spell_time = current_time

        for spell in spells[:]:
            if spell["type"] == "sun_black_spell":
                spell["rect"].x += SPELL_VEL
                if spell["rect"].colliderect(white_tiger):
                    white_tiger_health -= 10
                    white_tiger_health_rect.width = white_tiger_health * 3
                    spells.remove(spell)
                elif spell["rect"].x > WIDTH:
                    spells.remove(spell)

            elif spell["type"] == "air":
                spell["rect"].x -= SPELL_VEL
                if spell["rect"].colliderect(sun):
                    sun_health -= 10
                    sun_health_rect.width = sun_health * 3
                    spells.remove(spell)
                    wind_explosive_active = True
                    wind_explosive_pos = (sun.x, sun.y)
                elif spell["rect"].x < 0:
                    spells.remove(spell)

        for spell in spells[:]:
            for other_spell in spells[:]:
                if spell != other_spell and spell["rect"].colliderect(other_spell["rect"]):
                    if (spell["type"] == "sun_black_spell" and other_spell["type"] == "air") or \
                            (spell["type"] == "air" and other_spell["type"] == "sun_black_spell"):
                        spells.remove(spell)
                        spells.remove(other_spell)

        draw_IMG()    
        draw(sun, white_tiger, sun_health_rect, white_tiger_health_rect, spells)

        pygame.display.update()

        if sun_health <= 0:
            print("Game Over! Player has been defeated.")
            run = False
        elif white_tiger_health <= 0:
            print("Congratulations! You have completed the first level.")  
            run = True

        clock.tick(60) 

    pygame.quit()

main()
