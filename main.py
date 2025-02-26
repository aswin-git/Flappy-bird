import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GRAVITY = 0.5
FLAP_STRENGTH = 6.5
PIPE_SPEED = 3
PIPE_SPACING = 185
GAP_HEIGHT = 130
GROUND_Y = 450
BIRD_X = 50

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images
try:
    bird_img = pygame.image.load('bluebird-midflap.png')
    pipe_top_img = pygame.image.load('pipe-red-d.png')
    pipe_bottom_img = pygame.image.load('pipe-red.png')
    bg_img = pygame.image.load('background-day.png')
    ground_img = pygame.image.load('base.png')
except pygame.error as e:
    print(f"Error loading images: {e}")
    sys.exit()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for text rendering
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    """Render and display text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main():
    # Game variables
    bird_y = SCREEN_HEIGHT // 2  # Start bird in the middle
    bird_velocity = 0
    score = 0
    game_mode = 'start'
    pipe_list = []  # List of [x, gap_center, scored] for each pipe pair
    ground_x = 0

    # Main game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game_mode == 'start':
                    game_mode = 'playing'
                elif game_mode == 'playing':
                    bird_velocity = -FLAP_STRENGTH
                elif game_mode == 'game_over':
                    # Reset game
                    bird_y = SCREEN_HEIGHT // 2
                    bird_velocity = 0
                    pipe_list = []
                    score = 0
                    game_mode = 'playing'

        if game_mode == 'playing':
            # Update bird position
            bird_velocity += GRAVITY
            bird_y += bird_velocity

            # Move pipes
            for pipe in pipe_list:
                pipe[0] -= PIPE_SPEED

            # Remove pipes that are off-screen
            if pipe_list and pipe_list[0][0] < -pipe_top_img.get_width():
                pipe_list.pop(0)

            # Spawn new pipes
            if not pipe_list or pipe_list[-1][0] < SCREEN_WIDTH - PIPE_SPACING:
                gap_center = random.randint(100, 400)
                pipe_list.append([SCREEN_WIDTH, gap_center, False])

            # Collision detection
            bird_rect = pygame.Rect(BIRD_X, bird_y, bird_img.get_width() - 5, bird_img.get_height() - 5)  #Slightly smaller hitbox
            for pipe in pipe_list:
                top_pipe_y = pipe[1] - GAP_HEIGHT / 2 - pipe_top_img.get_height()
                bottom_pipe_y = pipe[1] + GAP_HEIGHT / 2
                top_pipe_rect = pygame.Rect(pipe[0], top_pipe_y, pipe_top_img.get_width(), pipe_top_img.get_height())
                bottom_pipe_rect = pygame.Rect(pipe[0], bottom_pipe_y, pipe_bottom_img.get_width(), pipe_bottom_img.get_height())
                if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect) or bird_y > GROUND_Y - bird_img.get_height():
                    game_mode = 'game_over'

            # Update score
            for pipe in pipe_list:
                if BIRD_X > pipe[0] + pipe_top_img.get_width() / 2 and not pipe[2]:
                    score += 1
                    pipe[2] = True

        # Drawing
        # Background
        screen.blit(bg_img, (0, 0))

        # Pipes
        for pipe in pipe_list:
            top_pipe_y = pipe[1] - GAP_HEIGHT / 2 - pipe_top_img.get_height()
            bottom_pipe_y = pipe[1] + GAP_HEIGHT / 2
            screen.blit(pipe_top_img, (pipe[0], top_pipe_y))
            screen.blit(pipe_bottom_img, (pipe[0], bottom_pipe_y))

        # Bird with rotation
        bird_rotation = max(min(-bird_velocity * 3, 30), -90)  # Clamp rotation between -90 and 30 degrees
        rotated_bird = pygame.transform.rotate(bird_img, bird_rotation)
        bird_rect = rotated_bird.get_rect(center=(BIRD_X + bird_img.get_width() // 2, bird_y + bird_img.get_height() // 2))
        screen.blit(rotated_bird, bird_rect.topleft)

        # Scrolling ground
        ground_x -= PIPE_SPEED
        if ground_x < -ground_img.get_width():
            ground_x = 0
        screen.blit(ground_img, (ground_x, GROUND_Y))
        screen.blit(ground_img, (ground_x + ground_img.get_width(), GROUND_Y))

        # Display score
        draw_text('Score: ' + str(score), SCREEN_WIDTH // 2, 50)

        # Game state overlays
        if game_mode == 'start':
            draw_text("Press Space to Start", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        elif game_mode == 'game_over':
            draw_text("Game Over", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, RED)
            draw_text(f"Score: {score}", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
            draw_text("Press Space to Restart", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)

        # Update display
        pygame.display.flip()
        clock.tick(59)  # 60 FPS

if __name__ == "__main__":
    main() 