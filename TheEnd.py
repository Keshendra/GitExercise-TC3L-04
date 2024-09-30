import pygame
import moviepy.editor as mp
import numpy as np
import sys
import os

def the_end_main():
    
    pygame.init()

    WIDTH, HEIGHT = 1200, 700

    background_video_path = "wall.mp4" 

    def check_file_exists(file_path):
        if os.path.isfile(file_path):
            print(f"File found: {file_path}")
            return True
        else:
            print(f"Error: The file '{file_path}' does not exist.")
            return False

    if not check_file_exists(background_video_path):
        pygame.quit()
        sys.exit()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MYSTIC QUEST")

    try:
        background_video = mp.VideoFileClip(background_video_path)
        print("Background video loaded successfully.")
    except OSError as e:
        print(f"Error: Could not load background video file. {e}")
        pygame.quit()
        sys.exit()

    font = pygame.font.SysFont('Copperplate Gothic Bold Black', 36)
    text_color = (255, 255, 255) 
    highlight_color = (0, 0, 0, 128) 

    final_story = [
        "Sun Wukong, after a long and perilous journey,",
        "defeated the four mighty guardians of the elements.",
        "The Red Bird, the Blue Dragon, the White Tiger, and the Black Tortoise,",
        "all fell to his strength, skill, and cunning.",
        "With balance restored to the world, Sun Wukong's legend",
        "as the hero who united the elements was cemented for eternity.",
        "And so, peace reigned once more..."
    ]

    STORY = 'story'
    END = 'end'
    state = STORY

    # Ensure start_time is a global variable
    global start_time
    start_time = pygame.time.get_ticks()

    # Function to draw text with typewriter effect
    def draw_highlighted_text(screen, text, font, color, highlight_color, max_width=1000, typing_speed=50):
        global start_time  # Declare as global to use the global start_time
        elapsed_time = (pygame.time.get_ticks() - start_time) // typing_speed  # Control typing speed
        total_characters = sum([len(line) for line in text])

        y_position = 150
        displayed_characters = 0
        lines = []

        for line in text:
            words = line.split()
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                test_surface = font.render(test_line, True, color)
                if test_surface.get_width() > max_width:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line

            if current_line:
                lines.append(current_line)

        # Draw highlight and typewriter text line by line
        for line in lines:
            if displayed_characters >= elapsed_time:
                break

            # Limit characters per line according to the elapsed time
            line_to_display = line[:max(0, elapsed_time - displayed_characters)]
            line_surface = font.render(line_to_display, True, color)
            line_rect = line_surface.get_rect(center=(WIDTH // 2, y_position))

            # Highlight background
            highlight_rect = pygame.Rect(line_rect.x - 10, line_rect.y - 5, line_rect.width + 20, line_rect.height + 10)
            highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
            highlight_surface.fill(highlight_color)

            # Draw the highlight and the text
            screen.blit(highlight_surface, highlight_rect.topleft)
            screen.blit(line_surface, line_rect)

            y_position += font.get_linesize() + 10
            displayed_characters += len(line)

    # Function to display the story page
    def draw_story_page():
        global start_time  # Ensure global usage
        current_time = (pygame.time.get_ticks() - start_time) / 1000
        if current_time >= background_video.duration:
            start_time = pygame.time.get_ticks()  # Reset start_time for looping
            current_time = 0

        try:
            frame = background_video.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
            frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"Error: Failed to display background video frame. {e}")

        # Draw the text with typewriter effect
        draw_highlighted_text(screen, final_story, font, text_color, highlight_color)

    def draw_end_screen():
        screen.fill((0, 0, 0)) 
        end_text = font.render("THE END", True, text_color)
        end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(end_text, end_rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if state == STORY:
            draw_story_page()
            if (pygame.time.get_ticks() - start_time) // 1000 > 18:  # After 18 seconds, move to the end screen
                state = END
                start_time = pygame.time.get_ticks()  # Reset start_time for end screen
        elif state == END:
            draw_end_screen()
            running = True 
            from Main import main
            main()

        pygame.display.update()

    background_video.close()

if __name__ == "__main__":
    the_end_main()
