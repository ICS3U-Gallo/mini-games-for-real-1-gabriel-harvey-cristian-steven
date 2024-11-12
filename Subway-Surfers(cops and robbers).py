import pygame
import random
import time  

pygame.init()

WIDTH, HEIGHT = 750, 900
GROUND_HEIGHT = 100
FPS = 60
immunity = False
immunityTime = 0
allowedImmunity = 150

# colors
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

# player variables
player_width, player_height = 50, 50  
player_x = WIDTH // 2
player_y = HEIGHT - GROUND_HEIGHT - player_height
player_speed = 10

# enemy (obstacle) variables
obstacle_width, obstacle_height = 250, 250  
obstacle_x = random.choice([0, 250, 500])  
obstacle_y = -obstacle_height  
obstacle_speed = 10  

# Shield variables
shield_radius = 30  # Shield size
shield_x = random.choice([100, 350, 600])  
shield_y = -shield_radius  
shield_speed = 5  
Shieldimmunity = False  
shield_immunity_start_time = 0  
shield_immunity_duration = 3  

# Player immunity variables (for hitting obstacles)
immunity_start_time = 0
immunity_duration = 3  
allowedImmunity = 150  

# score and lives
score = 0
lives = 3  
previous_score = 0

# game loop
running = True
clock = pygame.time.Clock()

# Draw the road vertically
def draw_road():
    lane_width = WIDTH // 3  

    # Draw the 3 lanes (dark grey)
    for i in range(3):
        pygame.draw.rect(screen, ROAD_COLOR, (i * lane_width, 0, lane_width, HEIGHT - GROUND_HEIGHT))

    # Draw dashed lines (vertical lane markings)
    line_spacing = 30
    line_width = 5  
    for i in range(0, HEIGHT - GROUND_HEIGHT, line_spacing * 2):  
        # Drawing vertical dashed lines in the middle of each lane
        pygame.draw.rect(screen, LINE_COLOR, (lane_width - line_width // 2, i + line_spacing, line_width, line_width))  
        pygame.draw.rect(screen, LINE_COLOR, (lane_width * 2 - line_width // 2, i + line_spacing, line_width, line_width))  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Shield immunity logic: Disable shield immunity after the set duration
    if Shieldimmunity and time.time() - shield_immunity_start_time >= shield_immunity_duration:
        Shieldimmunity = False  

    # Immunity logic: Disable immunity after the set duration (obstacle-induced immunity)
    if immunity and time.time() - immunity_start_time >= immunity_duration:
        immunity = False  

    if immunity == True and immunityTime >= allowedImmunity:
        immunity = False
        immunityTime = 0 
    elif immunity == True and immunityTime < allowedImmunity:
        immunityTime += 1

    # player input (left/right movement now)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:  
        player_x += player_speed

    # Ensure player doesn't move off the screen
    if player_x < 0:
        player_x = 0  
    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width  

    # move enemy down (fall from top to bottom)
    obstacle_y += obstacle_speed

    # move shield down (fall from top to bottom)
    if not Shieldimmunity:
        shield_y += shield_speed

    # check for collision with obstacle
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

    # Check for obstacle collision and apply temporary immunity
    if player_rect.colliderect(obstacle_rect) and not Shieldimmunity:
        if not immunity:  
            lives -= 1
            immunity = True
            immunity_start_time = time.time() 
            if lives == 0:
                running = False  
        obstacle_y = -obstacle_height  

    # check for shield collision with player
    shield_rect = pygame.Rect(shield_x, shield_y, shield_radius * 2, shield_radius * 2)
    if player_rect.colliderect(shield_rect):
        Shieldimmunity = True
        shield_immunity_start_time = time.time()  
        shield_y = -shield_radius  

    # update the score
    score += 1

    # Increase the obstacle speed when the score reaches a multiple of 1000
    if score // 1000 > previous_score // 1000:
        obstacle_speed += 5  
        previous_score = score  

    # check if the score reaches 5000 and end the game if it does
    if score >= 5000:
        running = False 

    # draw
    screen.fill(ROAD_COLOR)

    # Draw the road
    draw_road()

    # Draw the player (green rectangle or blue if immune from shield, red if immune from obstacle)
    if Shieldimmunity:
        pygame.draw.rect(screen, BLUE, player_rect)  
    elif immunity:  
        pygame.draw.rect(screen, RED, player_rect)
    else:
        pygame.draw.rect(screen, GREEN, player_rect)  

    # Draw the enemy (red rectangle)
    pygame.draw.rect(screen, RED, obstacle_rect)

    # Draw the shield (light blue circle)
    if not Shieldimmunity and shield_y > 0:  
        pygame.draw.circle(screen, LIGHT_BLUE, (shield_x + shield_radius, shield_y + shield_radius), shield_radius)

    # display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # display lives
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(lives_text, (10, 35))

    # display game over screen if player lost or score reached 5000
    if not running:
        font_large = pygame.font.Font(None, 72)
        game_over_text = font_large.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    pygame.display.flip()

    # Reset enemy position if it falls off the screen
    if obstacle_y > HEIGHT:
        obstacle_y = -obstacle_height 
        obstacle_x = random.choice([0, 250, 500])  

    # Reset shield position if it falls off the screen
    if shield_y > HEIGHT:
        shield_y = -shield_radius  
        shield_x = random.choice([100, 350, 600])  

    clock.tick(FPS)

# quit pygame
pygame.quit()
