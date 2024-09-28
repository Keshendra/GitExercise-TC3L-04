import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize mixer for background music
pygame.mixer.init()

# Screen dimensions
WIDTH = 1200
HEIGHT = 780

player_width = 80
player_height = 100
player_x = 100
player_y = HEIGHT - player_height - 10
player_speed = 5
player_y_velocity = 0

# Zhu Bajie's position on the top right platform
zhu_bajie_x = WIDTH - 200
zhu_bajie_y = 100 - player_height  # Adjusted for the new lowered platform

# Colors
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

zhu_bajie_image = pygame.image.load('zhu_bajie.png').convert_alpha()
zhu_bajie_image = pygame.transform.scale(zhu_bajie_image, (80, 100))

lava_image = pygame.image.load('air portal.png').convert_alpha()
lava_image = pygame.transform.scale(lava_image, (200, 50))

# Load life icon image
life_icon_image = pygame.image.load('air health.png').convert_alpha()
life_icon_image = pygame.transform.scale(life_icon_image, (30, 30))  # Adjust size as needed

# Load background music and play it in a loop (-1)
pygame.mixer.music.load("air backgroud.mp3")  # Replace with your music file
pygame.mixer.music.play(-1)  # -1 means the music will loop infinitely

GRAVITY = 1
jump_force = 15
can_double_jump = False

bullet_width = 20
bullet_height = 10
bullet_speed = 10
fire_minis = []
enemy_shooting_interval = 2000  # 2 seconds between shots
enemy_last_shot_time = 0

# Initialize player lives
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
        screen.blit(lava_image, (self.rect.x, self.rect.y))  # Draw lava image instead of rectangle

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
        screen.blit(life_icon_image, (10 + i * 40, 10))  # Adjust the position as needed

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

    screen.blit(zhu_bajie_image, (zhu_bajie_x, zhu_bajie_y))

    # Display the number of lives
    display_lives(lives)

    # Check if player meets Zhu Bajie for interaction
    zhu_bajie_rect = pygame.Rect(zhu_bajie_x, zhu_bajie_y, 50, 75)
    if player_rect.colliderect(zhu_bajie_rect) and not in_dialogue:
        # Trigger dialogue and stop fire mini
        stop_fire_minis = True

        if dialogue_stage < len(dialogues):  # Check if there's more dialogue
            sun_dialogue, bajie_dialogue = dialogues[dialogue_stage]
            if dialogue_stage % 2 == 0:
                display_dialogue(sun_dialogue, (player_x - 50, player_y - 40))
            else:
                display_dialogue(bajie_dialogue, (zhu_bajie_x - 50, zhu_bajie_y - 40))
            dialogue_timer += 1
            if dialogue_timer > 120:  # Show each dialogue for a certain period
                dialogue_stage += 1
                dialogue_timer = 0
        else:
            in_dialogue = False  # End dialogue after all stages are done
            stop_fire_minis = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
