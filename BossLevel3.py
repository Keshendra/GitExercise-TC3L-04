import pygame
import Maps

pygame.init()
pygame.mixer.init()
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

BG = pygame.image.load("water_bg.jpg").convert_alpha()
BG_img = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BL = pygame.image.load("bl.png").convert_alpha()
BL_img = pygame.transform.scale(BL, (BL_WIDTH, BL_HEIGHT))

sun = pygame.image.load("sun.png").convert_alpha()
sun_img = pygame.transform.scale(sun, (PLAYER_WIDTH, PLAYER_HEIGHT))

blue_dragon = pygame.image.load("blue_dragon.png").convert_alpha()
blue_dragon_img = pygame.transform.scale(blue_dragon, (PLAYER_WIDTH, PLAYER_HEIGHT))

water_spell_sound = pygame.mixer.Sound("watersound.mp3")
water_explosion_sound = pygame.mixer.Sound("waterexplosionsound.mp3")

blackmyth_spell_frames = [pygame.image.load(f"blackmyth_spell_frame_{i}.png").convert_alpha() for i in range(1, 10)]
current_blackmyth_frame = 0
frame_delay = 2  
frame_count = 0

water_spell_frames = [pygame.image.load(f"water_spell_frame_{i}.png").convert_alpha() for i in range(1, 7)]
current_water_frame = 0

water_explosive_frames = [pygame.image.load(f"water_explosive_frame_{i}.png").convert_alpha() for i in range(1, 16)]
blackmyth_explosive_frames = [pygame.image.load(f"blackmyth_explosive_frame_{i}.png").convert_alpha() for i in range(1, 9)]

explosive_active = False
explosive_pos = None
explosive_frame = 0
explosion_type = None 

def draw_IMG():
    WINDOW.blit(BG_img, (0, 0))
    WINDOW.blit(BL_img, (500, 0))

def draw(sun, blue_dragon, sun_health_rect, blue_dragon_health_rect, spells):
    global current_blackmyth_frame, current_water_frame, frame_count, explosive_active, explosive_frame, explosion_type
    WINDOW.blit(sun_img, (sun.x, sun.y))
    WINDOW.blit(blue_dragon_img, (blue_dragon.x, blue_dragon.y))

    for spell in spells:
        if spell["type"] == "blackmyth_spell":
            frame_count += 1
            if frame_count >= frame_delay:
                frame_count = 0
                current_blackmyth_frame = (current_blackmyth_frame + 1) % len(blackmyth_spell_frames)
            WINDOW.blit(blackmyth_spell_frames[current_blackmyth_frame], (spell["rect"].x, spell["rect"].y))

        elif spell["type"] == "water":
            frame_count += 1
            if frame_count >= frame_delay:
                frame_count = 0
                current_water_frame = (current_water_frame + 1) % len(water_spell_frames)
            WINDOW.blit(water_spell_frames[current_water_frame], (spell["rect"].x, spell["rect"].y))

        if explosive_active and explosive_pos:
            if explosion_type == "water":
                WINDOW.blit(water_explosive_frames[explosive_frame], explosive_pos)
            elif explosion_type == "blackmyth_spell":
                WINDOW.blit(blackmyth_explosive_frames[explosive_frame], explosive_pos)

            explosive_frame += 1
            if explosion_type == "water" and explosive_frame >= len(water_explosive_frames):
                explosive_active = False
                explosive_frame = 0
            elif explosion_type == "blackmyth_spell" and explosive_frame >= len(blackmyth_explosive_frames):
                explosive_active = False
                explosive_frame = 0    

    pygame.draw.rect(WINDOW, "green", sun_health_rect)
    pygame.draw.rect(WINDOW, "red", blue_dragon_health_rect)

def bosslevel_3_main():
    global explosive_active, explosive_pos, explosion_type

    run = True

    sun = pygame.Rect(50, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    blue_dragon = pygame.Rect(WIDTH - PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    sun_health = PLAYER_HEALTH
    blue_dragon_health = PLAYER_HEALTH
    sun_health_rect = pygame.Rect(10, 10, sun_health * 3, 40)
    blue_dragon_health_rect = pygame.Rect(WIDTH - 300 - 10, 10, 300, 40)

    spells = []
    last_blackmyth_spell_time = pygame.time.get_ticks()
    last_water_spell_time = pygame.time.get_ticks() 

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

        if keys[pygame.K_SPACE] and current_time - last_blackmyth_spell_time > 500:
            blackmyth_spell_rect = pygame.Rect(sun.x + sun.width, sun.y + sun.height // 2 - 150, 100, 100)
            spells.append({"type": "blackmyth_spell", "rect": blackmyth_spell_rect})
            last_blackmyth_spell_time = current_time

        if current_time - last_water_spell_time >= 1000:
            water_spell_rect = pygame.Rect(blue_dragon.x, blue_dragon.y + blue_dragon.height // 2 - 150, 100, 100)
            spells.append({"type": "water", "rect": water_spell_rect})
            water_spell_sound.play()
            last_water_spell_time = current_time

        for spell in spells[:]:
            if spell["type"] == "blackmyth_spell":
                spell["rect"].x += SPELL_VEL
                if spell["rect"].colliderect(blue_dragon):
                    blue_dragon_health -= 10
                    blue_dragon_health_rect.width = blue_dragon_health * 3
                    spells.remove(spell)
                    explosive_active = True
                    explosive_pos = (blue_dragon.x, blue_dragon.y)
                    explosion_type = "blackmyth_spell"
                elif spell["rect"].x > WIDTH:
                    spells.remove(spell)

            elif spell["type"] == "water":
                spell["rect"].x -= SPELL_VEL
                if spell["rect"].colliderect(sun):
                    sun_health -= 10
                    sun_health_rect.width = sun_health * 3
                    spells.remove(spell)
                    explosive_active = True
                    explosive_pos = (sun.x, sun.y)
                    explosion_type = "water"
                    water_explosion_sound.play()
                elif spell["rect"].x < 0:
                    spells.remove(spell)

        for spell in spells[:]:
            for other_spell in spells[:]:
                if spell != other_spell and spell["rect"].colliderect(other_spell["rect"]):
                    if (spell["type"] == "blackmyth_spell" and other_spell["type"] == "water") or \
                            (spell["type"] == "water" and other_spell["type"] == "blackmyth_spell"):
                        spells.remove(spell)
                        spells.remove(other_spell)

        draw_IMG()    
        draw(sun, blue_dragon, sun_health_rect, blue_dragon_health_rect, spells)

        pygame.display.update()

        if sun_health <= 0:
            run = True
        elif blue_dragon_health <= 0:
            run = False
            Maps.maps_main()

        clock.tick(60) 

if __name__ == "__main__":
    bosslevel_3_main()