import pygame
import random

pygame.init()

WIDTH, HEIGHT = 750, 900
GROUND_HEIGHT = 100
FPS = 60

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape the Cops")

# player variables
player_width, player_height = 50, 50  # Size of the player (as a rectangle)
player_x = WIDTH // 2
player_y = HEIGHT - GROUND_HEIGHT - player_height
player_speed = 10

# enemy (obstacle) variables
obstacle_width, obstacle_height = 250, 250  # Size of the obstacle (as a rectangle)
obstacle_x = random.choice([0, 250, 500])  # Randomize spawn in one of the three middle positions
obstacle_y = -obstacle_height  # Start above the screen (negative Y to make it fall down)
obstacle_speed = 20  # Speed at which the enemy falls down

# score
score = 0

# game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player input (left/right movement now)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  # Move player left
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:  # Move player right
        player_x += player_speed

    # Ensure player doesn't move off the screen
    if player_x < 0:
        player_x = 0  # Prevent moving past the left edge
    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width  # Prevent moving past the right edge

    # move enemy down (fall from top to bottom)
    obstacle_y += obstacle_speed

    # check for collision
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

    if player_rect.colliderect(obstacle_rect):
        running = False  # End the game on collision

    # update the score
    score += 1

    # check if the score reaches 5000 and end the game if it does
    if score >= 5000:
        running = False  # End the game if score reaches 5000

    # draw
    screen.fill(WHITE)

    # Draw the player (green rectangle)
    pygame.draw.rect(screen, GREEN, player_rect)

    # Draw the enemy (red rectangle)
    pygame.draw.rect(screen, RED, obstacle_rect)

    # display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # display game over screen if player lost or score reached 5000
    if not running:
        font_large = pygame.font.Font(None, 72)
        game_over_text = font_large.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    pygame.display.flip()

    # Reset enemy position if it falls off the screen
    if obstacle_y > HEIGHT:
        obstacle_y = -obstacle_height  # Reset to top of screen
        obstacle_x = random.choice([0, 250, 500])  # Randomize X position in one of the three areas

    clock.tick(FPS)

# quit pygame
pygame.quit()
