import pygame
import random
import BossLevel4

# Initialize Pygame
pygame.init()

# Initialize the mixer for playing sounds
pygame.mixer.init()

# Load background music
pygame.mixer.music.load('fire music.mp3')  # Make sure to have this file
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music in a loop

# Screen dimensions
WIDTH = 1200
HEIGHT = 600

player_width = 80
player_height = 100
player_x = 100
player_y = HEIGHT - player_height - 10 
player_speed = 5
player_y_velocity = 0

# Move Zhu Bajie to the top right
zhu_bajie_x = WIDTH - 150  # Adjusted for position
zhu_bajie_y = 50  # Adjusted height for the top right

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MYSTIC QUEST")

BG = pygame.image.load("fire_1bg.jpg").convert_alpha()
BG_img = pygame.transform.scale(BG, (WIDTH, HEIGHT))

player_image = pygame.image.load('sun_moving.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height))

fire_mini_image = pygame.image.load('fire_mini.png').convert_alpha()
fire_mini_image = pygame.transform.scale(fire_mini_image, (50, 50))

zhu_bajie_image = pygame.image.load('zhu_bajie.png').convert_alpha()
zhu_bajie_image = pygame.transform.scale(zhu_bajie_image, (80, 100)) 

lava_image = pygame.image.load('lava.png').convert_alpha()
lava_image = pygame.transform.scale(lava_image, (200, 50)) 

# Load life icon image
life_image = pygame.image.load('fire health.png').convert_alpha()
life_image = pygame.transform.scale(life_image, (30, 30))  # Adjust size as needed

GRAVITY = 1
jump_force = 15
can_double_jump = False

bullet_width = 20
bullet_height = 10
bullet_speed = 5
fire_minis = []
enemy_shooting_interval = 1000
enemy_last_shot_time = 0

game_over = False 
lives = 3  

class Platform:
    def __init__(self, x, y, width, height, speed=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed 
        self.direction = 1 

    def move(self):
        # Move platform horizontally
        self.rect.x += self.speed * self.direction

        # Reverse direction if the platform hits the edge of the screen or moves too far
        if self.rect.x <= 0 or self.rect.x + self.rect.width >= WIDTH:
            self.direction *= -1

    def draw(self):
        screen.blit(lava_image, (self.rect.x, self.rect.y))  

# Platforms with horizontal movement
platforms = [
    Platform(100, HEIGHT - 100, 200, 10, speed=2),
    Platform(400, HEIGHT - 200, 200, 10, speed=3),
    Platform(600, HEIGHT - 300, 200, 10, speed=2),
    Platform(750, HEIGHT - 400, 200, 10, speed=4),
    Platform(300, HEIGHT - 500, 200, 10, speed=1),  
    Platform(500, HEIGHT - 600, 200, 10, speed=3),  
    Platform(900, HEIGHT - 700, 200, 10, speed=2), 
    # Add a non-movable platform for Zhu Bajie
    Platform(WIDTH - 200, zhu_bajie_y + 80, 150, 10, speed=0), 
]

dialogue_timer = 0 
def display_dialogue(text, position):
    font = pygame.font.SysFont(None, 30)
    dialogue_surface = font.render(text, True, BLACK)
    screen.blit(dialogue_surface, position)

def display_lives():
    for i in range(lives):
        screen.blit(life_image, (10 + i * 35, 10))  # Display lives at the top-left corner

def platform_4_main():
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

        if game_over:
            font = pygame.font.SysFont(None, 74)
            game_over_surface = font.render("Game Over", True, BLACK)
            screen.blit(game_over_surface, (WIDTH//2 - 150, HEIGHT//2 - 50))
            pygame.display.flip()
            continue 

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            if player_y_velocity == 0:
                player_y_velocity = -jump_force
                can_double_jump = True
            elif can_double_jump:
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
            if player_rect.colliderect(platform.rect):
                player_y_velocity = 0
                player_y = platform.rect.top - player_height

        # Player can't fall below the ground
        if player_y > HEIGHT - player_height:
            player_y = HEIGHT - player_height
            player_y_velocity = 0

        # Move and draw platforms
        for platform in platforms:
            platform.move() 
            platform.draw()

        # Enemy shooting logic (from right-hand side)
        current_time = pygame.time.get_ticks()
        if not stop_fire_minis: 
            if current_time - enemy_last_shot_time > enemy_shooting_interval:
                enemy_last_shot_time = current_time
                for _ in range(2): 
                    fire_mini = pygame.Rect(WIDTH, random.randint(100, HEIGHT - bullet_height), bullet_width, bullet_height)
                    fire_minis.append(fire_mini)

        # Move enemy bullets (fire mini)
        for fire_mini in fire_minis:
            fire_mini.x -= bullet_speed
        fire_minis = [fire_mini for fire_mini in fire_minis if fire_mini.x > 0]

        # Collision detection between player and fire mini bullets
        for fire_mini in fire_minis[:]:
            if player_rect.colliderect(fire_mini):
                fire_minis.remove(fire_mini) 
                lives -= 1  # 
                print("Player hit by fire mini! Lives left:", lives)
                if lives <= 0:
                    game_over = True

        # Draw fire mini (enemy bullets) using the image
        if not stop_fire_minis:
            for fire_mini in fire_minis:
                screen.blit(fire_mini_image, (fire_mini.x, fire_mini.y))

        screen.blit(player_image, (player_x, player_y))
        screen.blit(zhu_bajie_image, (zhu_bajie_x, zhu_bajie_y))

        # Check for player interaction with Zhu Bajie
        if player_rect.colliderect(pygame.Rect(zhu_bajie_x, zhu_bajie_y, 80, 100)):
            in_dialogue = True
            if dialogue_stage < len(dialogues):
                if dialogue_timer == 0:
                    display_dialogue(dialogues[dialogue_stage][0], (zhu_bajie_x - 50, zhu_bajie_y - 50)) 
                else:
                    display_dialogue(dialogues[dialogue_stage][1], (zhu_bajie_x - 50, zhu_bajie_y - 50))

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
            BossLevel4.bosslevel_4_main()

        display_lives() 

        pygame.display.flip()  
        clock.tick(60) 

if __name__ == "__main__":
    platform_4_main()