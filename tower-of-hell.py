import pygame
import time

pygame.init()

# Screen settings
WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Load sounds
death_sound = pygame.mixer.Sound("game_over.mp3")
pygame.mixer.music.load("escape.mp3")
pygame.mixer.music.play(-1)

# Initialize global variables
mario_x = 500
mario_y = 400
mario_speed = 10
velocity_y = 0
gravity = 5
ground = False
death = False
death_animation = False
death_velocity = 0
level = 1  # Starting level

# Define platforms, walls, and killbricks for each level
def load_stage(level):
    global platforms, killbricks, walls, mario_y
    if level == 1:
        platforms = [
            (470, 430, 150, 10),
            (275, 400, 150, 10),
            (111, 369, 150, 10),
            (111, 309, 150, 10),
            (280, 270, 340, 10),
            (575, 190, 50, 10),
            (525, 130, 50, 10),
            (575, 80, 50, 10),
            (575, 30, 50, 10)
        ]
        killbricks = [
            (340, 380.5, 20, 20),
            (241, 289.9, 20, 20),
            (111, 289.9, 20, 20)
        ] + [(x, 255, 15, 15) for x in range(300, 600, 75)]
        walls = [(-30, -20, 50, 1000), (620, -20, 50, 1000)]
    elif level == 2:
        platforms = [
            (50, 400, 150, 10),
            (200, 350, 150, 10),
            (350, 300, 150, 10),
            (500, 250, 150, 10)
        ]
        killbricks = [
            (100, 380, 20, 20),
            (300, 340, 20, 20),
            (450, 280, 20, 20)
        ]
        walls = [(-30, -20, 50, 1000), (620, -20, 50, 1000)]

# Load the initial stage
load_stage(level)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)

    # Game state updates
    if not death_animation and not death:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mario_x -= mario_speed
        if keys[pygame.K_RIGHT]:
            mario_x += mario_speed
        if keys[pygame.K_SPACE] and ground:
            velocity_y = -25  # Jump strength
            ground = False    

        if not ground:
            velocity_y += gravity

        mario_y += velocity_y

        mario_rect = pygame.Rect(mario_x, mario_y, 15, 25)

        ground = False  # Assume Mario is in the air
        for platform in platforms:
            platform_rect = pygame.Rect(platform)
            if mario_rect.colliderect(platform_rect) and velocity_y >= 0:
                mario_y = platform_rect.top - mario_rect.height 
                velocity_y = 0
                ground = True
                break

        for wall in walls:
            wall_rect = pygame.Rect(wall)
            if mario_rect.colliderect(wall_rect):
                if mario_rect.right > wall_rect.left and mario_rect.left < wall_rect.left:
                    mario_x = wall_rect.left - mario_rect.width
                elif mario_rect.left < wall_rect.right and mario_rect.right > wall_rect.right:
                    mario_x = wall_rect.right

        for kill in killbricks:
            kill_rect = pygame.Rect(kill)
            if mario_rect.colliderect(kill_rect):
                pygame.mixer.music.stop()
                death_animation = True
                death_velocity = -25
                death_sound.play()
                print("Game Over!")
                time.sleep(0.5)

        if mario_y > HEIGHT + 30:
            pygame.mixer.music.stop()
            death_animation = True
            death_sound.play()
            print("Game Over!")

        # Check if Mario goes above the screen
        if mario_y < 0:
            level += 1  # Go to the next level
            load_stage(level)  # Load the next stage

    else:
        death_velocity += gravity
        mario_y += death_velocity

        mario_rect = pygame.Rect(mario_x, mario_y, 15, 25)

        if mario_y > HEIGHT + 100:
            pygame.time.delay(int(death_sound.get_length() * 1000))   
            running = False

    # Drawing
    screen.fill((36, 40, 64))

    # Draw killbricks
    for kill in killbricks:
        pygame.draw.rect(screen, (255, 0, 0), kill)

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, (64, 64, 64), platform)

    # Draw tower walls
    for wall in walls:
        pygame.draw.rect(screen, (74, 74, 74), wall)

    # Draw Mario
    pygame.draw.rect(screen, (66, 66, 66), (mario_x, mario_y, 15, 15))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 2.5, mario_y - 10, 10, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 2, mario_y + 15, 4, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 9, mario_y + 15, 4, 10))

    # Refresh the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
