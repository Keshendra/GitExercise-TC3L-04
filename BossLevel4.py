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

BG = pygame.image.load("fire_bg.jpg").convert_alpha()
BG_img = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BL = pygame.image.load("bl.png").convert_alpha()
BL_img = pygame.transform.scale(BL, (BL_WIDTH, BL_HEIGHT))

sun = pygame.image.load("sun.png").convert_alpha()
sun_img = pygame.transform.scale(sun, (PLAYER_WIDTH, PLAYER_HEIGHT))

red_bird = pygame.image.load("red_bird.png").convert_alpha()
red_bird_img = pygame.transform.scale(red_bird, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Loading spell animation frames
blackmyth_spell_frames = [pygame.image.load(f"blackmyth_spell_frame_{i}.png").convert_alpha() for i in range(1, 10)]
current_blackmyth_frame = 0
frame_delay = 2  # Delay between frames to slow down animation
frame_count = 0

# Fire spell frames
fire_spell_frames = [pygame.image.load(f"fire_spell_frame_{i}.png").convert_alpha() for i in range(1, 9)]
current_fire_frame = 0

# Explosion frames for both spells
fire_explosive_frames = [pygame.image.load(f"fire_explosive_frame_{i}.png").convert_alpha() for i in range(1, 11)]
blackmyth_explosive_frames = [pygame.image.load(f"blackmyth_explosive_frame_{i}.png").convert_alpha() for i in range(1, 9)]

explosive_active = False
explosive_pos = None
explosive_frame = 0
explosion_type = None  # Keep track of which spell caused the explosion

def draw_IMG():
    WINDOW.blit(BG_img, (0, 0))
    WINDOW.blit(BL_img, (400, 0))

def draw(sun, red_bird, sun_health_rect, red_bird_health_rect, spells):
    global current_blackmyth_frame, current_fire_frame, frame_count, explosive_active, explosive_frame, explosion_type

    # Draw players
    WINDOW.blit(sun_img, (sun.x, sun.y))
    WINDOW.blit(red_bird_img, (red_bird.x, red_bird.y))

    # Draw spells
    for spell in spells:
        if spell["type"] == "blackmyth_spell":
            # Animate blackmyth spell
            frame_count += 1
            if frame_count >= frame_delay:
                frame_count = 0
                current_blackmyth_frame = (current_blackmyth_frame + 1) % len(blackmyth_spell_frames)
            WINDOW.blit(blackmyth_spell_frames[current_blackmyth_frame], (spell["rect"].x, spell["rect"].y))

        elif spell["type"] == "fire":
            # Animate fire spell
            frame_count += 1
            if frame_count >= frame_delay:
                frame_count = 0
                current_fire_frame = (current_fire_frame + 1) % len(fire_spell_frames)
            WINDOW.blit(fire_spell_frames[current_fire_frame], (spell["rect"].x, spell["rect"].y))

    # Draw explosions if active
    if explosive_active and explosive_pos:
        if explosion_type == "fire":
            WINDOW.blit(fire_explosive_frames[explosive_frame], explosive_pos)
        elif explosion_type == "blackmyth_spell":
            WINDOW.blit(blackmyth_explosive_frames[explosive_frame], explosive_pos)

        explosive_frame += 1
        if explosion_type == "fire" and explosive_frame >= len(fire_explosive_frames):
            explosive_active = False
            explosive_frame = 0
        elif explosion_type == "blackmyth_spell" and explosive_frame >= len(blackmyth_explosive_frames):
            explosive_active = False
            explosive_frame = 0

    # Draw health bars
    pygame.draw.rect(WINDOW, "green", sun_health_rect)
    pygame.draw.rect(WINDOW, "red", red_bird_health_rect)

def bosslevel_4_main():
    global explosive_active, explosive_pos, explosion_type

    run = True

    sun = pygame.Rect(50, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    red_bird = pygame.Rect(WIDTH - PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    sun_health = PLAYER_HEALTH
    red_bird_health = PLAYER_HEALTH
    sun_health_rect = pygame.Rect(10, 10, sun_health * 3, 40)
    red_bird_health_rect = pygame.Rect(WIDTH - 300 - 10, 10, 300, 40)

    spells = []
    last_blackmyth_spell_time = pygame.time.get_ticks()
    last_fire_spell_time = pygame.time.get_ticks()

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

        # Blackmyth spell (sun's spell)
        if keys[pygame.K_SPACE] and current_time - last_blackmyth_spell_time > 500:
            # Adjusted y-position of the blackmyth spell to be centered more appropriately
            blackmyth_spell_rect = pygame.Rect(sun.x + sun.width, sun.y + sun.height // 2 - 150, 100, 100)
            spells.append({"type": "blackmyth_spell", "rect": blackmyth_spell_rect})
            last_blackmyth_spell_time = current_time

        # Fire spell (red bird's spell)
        if current_time - last_fire_spell_time >= 1000:
            fire_spell_rect = pygame.Rect(red_bird.x, red_bird.y + red_bird.height // 2 - 150, 200, 200)
            spells.append({"type": "fire", "rect": fire_spell_rect})
            last_fire_spell_time = current_time

        # Update spell positions and check for collisions
        for spell in spells[:]:
            if spell["type"] == "blackmyth_spell":
                spell["rect"].x += SPELL_VEL
                if spell["rect"].colliderect(red_bird):
                    red_bird_health -= 10
                    red_bird_health_rect.width = red_bird_health * 3
                    spells.remove(spell)
                    # Trigger explosion
                    explosive_active = True
                    explosive_pos = (red_bird.x, red_bird.y)
                    explosion_type = "blackmyth_spell"
                elif spell["rect"].x > WIDTH:
                    spells.remove(spell)

            elif spell["type"] == "fire":
                spell["rect"].x -= SPELL_VEL
                if spell["rect"].colliderect(sun):
                    sun_health -= 10
                    sun_health_rect.width = sun_health * 3
                    spells.remove(spell)
                    # Trigger explosion
                    explosive_active = True
                    explosive_pos = (sun.x, sun.y)
                    explosion_type = "fire"
                elif spell["rect"].x < 0:
                    spells.remove(spell)

        # Check for collisions between spells
        for spell in spells[:]:
            for other_spell in spells[:]:
                if spell != other_spell and spell["rect"].colliderect(other_spell["rect"]):
                    if (spell["type"] == "blackmyth_spell" and other_spell["type"] == "fire") or \
                            (spell["type"] == "fire" and other_spell["type"] == "blackmyth_spell"):
                        spells.remove(spell)
                        spells.remove(other_spell)

        draw_IMG()
        draw(sun, red_bird, sun_health_rect, red_bird_health_rect, spells)

        pygame.display.update()

        if sun_health <= 0:
            print("Game Over! Player has been defeated.")
            run = False
        elif red_bird_health <= 0:
            print("Congratulations! You have completed the first level.")
            run = True

        clock.tick(60)

if __name__ == "__main__":
    bosslevel_4_main()

    pygame.quit()