import pygame
import random
import time
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 750, 900
GROUND_HEIGHT = 100
FPS = 60
immunity = False
immunityTime = 0
allowedImmunity = 150
running = True

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape the Cops")

# Player variables
player_width, player_height = 50, 50
player_x = WIDTH // 2
player_y = HEIGHT - GROUND_HEIGHT - player_height
player_speed = 10

# Enemy (obstacle) variables
obstacle_width, obstacle_height = 250, 250
obstacle_x = random.choice([0, 250, 500])
obstacle_y = -obstacle_height
obstacle_speed = 10

# Shield variables
shield_radius = 30
shield_x = random.choice([100, 350, 600])
shield_y = -shield_radius
shield_speed = 5
Shieldimmunity = False
shield_immunity_start_time = 0
shield_immunity_duration = 2.5
shieldOnScreen = False
shield_spawned = False

# Player immunity variables (for hitting obstacles)
immunity_start_time = 0
immunity_duration = 3
allowedImmunity = 150

# Score and lives
score = 0
lives = 3
previous_score = 0

# Game states
STATE_MENU = 0
STATE_GAME = 1
STATE_WIN = 2  # New game state for the win screen

# Initialize fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Draw the road vertically
def draw_road():
    lane_width = WIDTH // 3

    for i in range(3):
        pygame.draw.rect(screen, ROAD_COLOR, (i * lane_width, 0, lane_width, HEIGHT - GROUND_HEIGHT))

    line_spacing = 30
    line_width = 5
    for i in range(0, HEIGHT - GROUND_HEIGHT, line_spacing * 2):
        pygame.draw.rect(screen, LINE_COLOR, (lane_width - line_width // 2, i + line_spacing, line_width, line_width))
        pygame.draw.rect(screen, LINE_COLOR, (lane_width * 2 - line_width // 2, i + line_spacing, line_width, line_width))

# Draw the menu screen
def draw_menu():
    screen.fill(BLACK)

    title_text = big_font.render("Welcome to Escape the Cops!", True, GREEN)
    start_text = font.render("Press ENTER to Start", True, WHITE)
    controls_text = font.render("Use LEFT/RIGHT Arrow to Move", True, WHITE)
    shield_text = font.render("The blue orb grants you a shield ", True, WHITE)
    game_text = font.render("Goal is to reach 5000km", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 250))
    screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, 300))
    screen.blit(shield_text, (WIDTH //2 - shield_text.get_width() // 2, 350))
    screen.blit(game_text, (WIDTH // 2 - game_text.get_width() // 2, 400))

    pygame.display.flip()

# Draw the win screen
def draw_win():
    screen.fill(BLACK)

    win_text = big_font.render("You Have Escapsed!", True, GREEN)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press ENTER to Play Again", True, WHITE)

    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

# Draw the game screen
def draw_game():
    screen.fill(ROAD_COLOR)
    draw_road()

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    if Shieldimmunity:
        pygame.draw.rect(screen, BLUE, player_rect)
    elif immunity:
        pygame.draw.rect(screen, RED, player_rect)
    else:
        pygame.draw.rect(screen, GREEN, player_rect)

    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    
    # Draw car body
    pygame.draw.rect(screen, BLUE, (obstacle_x, obstacle_y, 250, 250))
    # Draw windows
    pygame.draw.rect(screen, WHITE, (obstacle_x + 30, obstacle_y + 50, 80, 60))
    pygame.draw.rect(screen, WHITE, (obstacle_x + 135, obstacle_y + 50, 80, 60))
    # Draw wheels
    pygame.draw.circle(screen, BLACK, (obstacle_x + 20, obstacle_y + 240), 15)
    pygame.draw.circle(screen, BLACK, (obstacle_x + 230, obstacle_y + 240), 15)

    if shield_spawned:
        pygame.draw.circle(screen, LIGHT_BLUE, (shield_x + shield_radius, shield_y + shield_radius), shield_radius)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 35))

    if not running:
        font_large = pygame.font.Font(None, 72)
        game_over_text = font_large.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    pygame.display.flip()

# Main game loop
def main():
    global player_x, obstacle_x, obstacle_y, shield_x, shield_y, shield_spawned, immunity, immunity_start_time, lives, score, obstacle_speed, previous_score, Shieldimmunity, shield_immunity_start_time

    clock = pygame.time.Clock()
    game_state = STATE_MENU  

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # reset lives
            if lives == 0:
                lives = 3

            #reset score
            if game_state == STATE_MENU:
                score = 0
                obstacle_speed = 10

            if event.type == pygame.KEYDOWN:
                if game_state == STATE_MENU:
                    if event.key == pygame.K_RETURN:  
                        game_state = STATE_GAME
                elif game_state == STATE_WIN:
                    if event.key == pygame.K_RETURN:  
                        game_state = STATE_MENU
                        score = 0
                        obstacle_speed = 10
                        lives = 3

        # Shield immunity logic: Disable shield immunity after the set duration             
        if Shieldimmunity and time.time() - shield_immunity_start_time >= shield_immunity_duration:
            Shieldimmunity = False 

        # Immunity logic: Disable immunity after the set duration (obstacle-induced immunity)
        if immunity and time.time() - immunity_start_time >= immunity_duration:
            immunity = False  

        # Ensure player doesn't move off the screen
        if player_x < 0:
            player_x = 0
        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

        #player movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:  
            player_x += player_speed

        # Game loop (STATE_GAME)
        if game_state == STATE_MENU:
            draw_menu()
        elif game_state == STATE_GAME:
            # Move enemy (obstacle) down
            obstacle_y += obstacle_speed

            # Move shield down
            if shield_spawned:
                shield_y += shield_speed

            # Check for shield spawn
            if not shield_spawned and random.random() < 0.005:
                shield_y > HEIGHT
                shield_x = random.choice([100, 350, 600])
                shield_y = -shield_radius
                shield_spawned = True

            # Check for collisions
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

            if player_rect.colliderect(obstacle_rect) and not Shieldimmunity:
                if not immunity:
                    lives -= 1
                    immunity = True
                    immunity_start_time = time.time()
                    if lives == 0:
                        game_state = STATE_MENU  
                obstacle_y = -obstacle_height

            # Check for shield collision with player
            shield_rect = pygame.Rect(shield_x, shield_y, shield_radius * 2, shield_radius * 2)
            if player_rect.colliderect(shield_rect):
                Shieldimmunity = True
                shield_immunity_start_time = time.time()
                shield_spawned = False

            # Update score
            score += 1

            # Increase difficulty based on score
            if score // 1000 > previous_score // 1000:
                obstacle_speed += 5
                previous_score = score

            # End game if score reaches 5000
            if score >= 5000:
                game_state = STATE_WIN

            # Draw the game screen
            draw_game()

            # Reset obstacle if it falls off the screen
            if obstacle_y > HEIGHT:
                obstacle_y = -obstacle_height
                obstacle_x = random.choice([0, 250, 500])

        elif game_state == STATE_WIN:
            draw_win()

        clock.tick(FPS)  

if __name__ == "__main__":
    main()
