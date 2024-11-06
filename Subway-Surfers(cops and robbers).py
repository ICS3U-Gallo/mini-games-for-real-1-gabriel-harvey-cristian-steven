import pygame

pygame.init()

WIDTH, HEIGHT = 800, 400
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
player_speed = 5
player_jump = False
jump_velocity = 15  # Initial velocity when jumping
fall_velocity = 0  # Initial falling velocity

# obstacle variables
obstacle_width, obstacle_height = 50, 50  # Size of the obstacle (as a rectangle)
obstacle_x = WIDTH
obstacle_y = HEIGHT - GROUND_HEIGHT - obstacle_height
obstacle_speed = 3

# score
score = 0

# game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP] and not player_jump:
        player_jump = True
        fall_velocity = 0  # Reset fall velocity when jumping

    # player jumping/falling
    if player_jump:
        player_y -= jump_velocity
        jump_velocity -= 1
        if jump_velocity < -15:
            player_jump = False
            jump_velocity = 15  # Reset jump height after the jump
    else:
        if player_y < HEIGHT - GROUND_HEIGHT - player_height:
            player_y += fall_velocity
            fall_velocity += 1  # Gravity
        else:
            player_y = HEIGHT - GROUND_HEIGHT - player_height
            fall_velocity = 0  # Reset fall velocity when reaching the ground

    # move obstacles
    obstacle_x -= obstacle_speed

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

    # Draw the obstacle (red rectangle)
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

    # check if obstacle is off screen
    if obstacle_x < -obstacle_width:
        obstacle_x = WIDTH
        obstacle_y = HEIGHT - GROUND_HEIGHT - obstacle_height

    clock.tick(FPS)

# quit pygame
pygame.quit()
