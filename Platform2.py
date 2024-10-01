import pygame
import random
import BossLevel2

pygame.init()        
pygame.mixer.init()

WIDTH = 1200
HEIGHT = 600

player_width = 80
player_height = 100
player_x = 100
player_y = HEIGHT - player_height - 10
player_speed = 5
player_y_velocity = 0

# Zhu Bajie's position on the top right platform
zha_wujiang_x = WIDTH - 200
zha_wujiang_y = 100 - player_height

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

BG = pygame.image.load("air background.png").convert_alpha()
BG_img = pygame.transform.scale(BG, (WIDTH, HEIGHT))

player_image = pygame.image.load('sun_moving.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height))

fire_mini_image = pygame.image.load('air_mini.png').convert_alpha()
fire_mini_image = pygame.transform.scale(fire_mini_image, (50, 50))

zha_wujiang_image = pygame.image.load('zha_wujiang.png').convert_alpha()
zha_wujiang_image = pygame.transform.scale(zha_wujiang_image, (80, 100))

lava_image = pygame.image.load('air portal.png').convert_alpha()
lava_image = pygame.transform.scale(lava_image, (200, 50))

# Load life icon image
life_icon_image = pygame.image.load('air health.png').convert_alpha()
life_icon_image = pygame.transform.scale(life_icon_image, (30, 30))

# Load background music and play it in a loop (-1)
pygame.mixer.music.load("air backgroud.mp3")
pygame.mixer.music.play(-1)

GRAVITY = 1
jump_force = 15
can_double_jump = False

bullet_width = 20
bullet_height = 10
bullet_speed = 10
fire_minis = []
enemy_shooting_interval = 2000
enemy_last_shot_time = 0

lives = 2

class Platform:
    def __init__(self, x, y, width, height, speed=0, min_y=None, max_y=None, is_moving=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.min_y = min_y if min_y is not None else y
        self.max_y = max_y if max_y is not None else y
        self.is_moving = is_moving
        self.direction = 1  # 1 for down, -1 for up

    def move(self):
        if self.is_moving:
            self.rect.y += self.speed * self.direction
            if self.rect.y <= self.min_y or self.rect.y >= self.max_y:
                self.direction *= -1

    def draw(self):
        screen.blit(lava_image, (self.rect.x, self.rect.y))

# Updated platform positions, including Zhu Bajie's platform
platforms = [
    Platform(50, HEIGHT - 150, 150, 10, 2, HEIGHT - 250, HEIGHT - 100),   # Lower platform, moving up and down
    Platform(300, HEIGHT - 250, 250, 10, 3, HEIGHT - 350, HEIGHT - 150),  # Middle platform, moving up and down
    Platform(600, HEIGHT - 180, 200, 10, 2, HEIGHT - 280, HEIGHT - 100),  # Higher platform, moving up and down
    Platform(800, HEIGHT - 350, 180, 10, 4, HEIGHT - 450, HEIGHT - 250),  # Higher platform, moving up and down
    Platform(WIDTH - 250, 100, 200, 10, is_moving=False)                   # Non-moving platform at the top right corner (lowered)
]

dialogue_timer = 0
def display_dialogue(text, position):
    font = pygame.font.SysFont(None, 30)
    dialogue_surface = font.render(text, True, BLACK)
    screen.blit(dialogue_surface, position)

def display_lives(lives):
    for i in range(lives):
        screen.blit(life_icon_image, (10 + i * 40, 10))

def platform_2_main():    
    global player_x, player_y, player_y_velocity, can_double_jump, game_over, lives
    global enemy_last_shot_time, fire_minis, in_dialogue, stop_fire_minis, dialogue_stage
    global dialogue_timer

running = True
in_dialogue = False  # Flag for Zhu Bajie interaction
dialogue_stage = 0   # Stage of dialogue (0: Sun speaks, 1: Zhu Bajie responds)
stop_fire_minis = False  # Flag to stop fire minis when Sun and Zhu Bajie meet

dialogues = [
    ("Sun: We must hurry to the next stage!", "Zhu Bajie: Yes, let's go quickly!"),
    ("Sun: Watch out for the lava!", "Zhu Bajie: I'm trying, but it's hot!"),
    ("Sun: We're getting close!", "Zhu Bajie: Don't get distracted now!"),
    ("Sun: Do you see the fire ahead?", "Zhu Bajie: We must be careful!")
]
    
while running:
    screen.blit(BG_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if player_y_velocity == 0:  # Regular jump
            player_y_velocity = -jump_force
            can_double_jump = True
        elif can_double_jump:  # Double jump
            player_y_velocity = -jump_force
            can_double_jump = False

    # Apply gravity to the player
    player_y_velocity += GRAVITY
    player_y += player_y_velocity

    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width

    # Prevent player from moving off the top of the screen
    if player_y < 0:
        player_y = 0
        player_y_velocity = 0

    # Check for collision with platforms
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for platform in platforms:
        platform.move()  # Move the platform if it's a moving one
        if player_rect.colliderect(platform.rect):
            player_y_velocity = 0
            player_y = platform.rect.top - player_height

    # Player can't fall below the ground
    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_y_velocity = 0

    for platform in platforms:
        platform.draw()

    # Enemy shooting logic (from right-hand side)
    current_time = pygame.time.get_ticks()
    if not stop_fire_minis:  # Only allow fire minis if not in dialogue
        if current_time - enemy_last_shot_time > enemy_shooting_interval:
            enemy_last_shot_time = current_time
            fire_mini = pygame.Rect(WIDTH, random.randint(100, HEIGHT - bullet_height), bullet_width, bullet_height)
            fire_minis.append(fire_mini)

    # Move enemy bullets (fire mini)
    for fire_mini in fire_minis:
        fire_mini.x -= bullet_speed
    fire_minis = [fire_mini for fire_mini in fire_minis if fire_mini.x > 0]

    # Collision detection between player and fire mini bullets
    for fire_mini in fire_minis[:]:
        if player_rect.colliderect(fire_mini):
            fire_minis.remove(fire_mini)  # Remove fire mini upon collision
            lives -= 1  # Reduce lives
            print("Player hit by Air mini!")  # For debugging purposes
            if lives <= 0:
                print("Game Over!")  # End the game if no lives left
                running = False

    # Draw fire mini (enemy bullets) using the image
    if not stop_fire_minis:
        for fire_mini in fire_minis:
            screen.blit(fire_mini_image, (fire_mini.x, fire_mini.y))

    screen.blit(player_image, (player_x, player_y))
    screen.blit(zha_wujiang_image, (zha_wujiang_x, zha_wujiang_y))

    if player_rect.colliderect(pygame.Rect(zha_wujiang_x, zha_wujiang_y, 80, 100)):
            in_dialogue = True
            if dialogue_stage < len(dialogues):
                if dialogue_timer == 0:
                    display_dialogue(dialogues[dialogue_stage][0], (zha_wujiang_x - 50, zha_wujiang_y - 50)) 
                else:
                    display_dialogue(dialogues[dialogue_stage][1], (zha_wujiang_x - 50, zha_wujiang_y - 50))

                # Increment dialogue stage after 2 seconds
                dialogue_timer += clock.get_time()
                if dialogue_timer > 2000: 
                    dialogue_timer = 0
                    dialogue_stage += 1

                if dialogue_stage >= len(dialogues):
                    dialogue_stage = 0
                    in_dialogue = False
                    stop_fire_minis = False

    if in_dialogue:
        running = True 
        BossLevel2.bosslevel_2_main()

    display_lives(lives) 

    pygame.display.flip()
    clock.tick(60)

if __name__ == "__main__":
    platform_2_main()