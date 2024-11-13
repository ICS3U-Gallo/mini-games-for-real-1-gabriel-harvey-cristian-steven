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
mario_spawn_x = 500
mario_spawn_y = 400
mario_speed = 10
velocity_y = 0
gravity = 5
ground = False
death = False
death_animation = False
death_velocity = 0
mario_x = mario_spawn_x
mario_y = mario_spawn_y
level = 1
sweeping_killbrick = None  # Initialize to None by default
sweeping_speed = 10
sweeping_direction = 1 
moving_platform = None
moving_speed = 5

# Define platforms, walls, and killbricks for each level
def load_stage(level):
    global platforms, killbricks, walls, mario_y, moving_platform, sweeping_killbrick
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
        moving_platform = None  # No moving platform in level 1
        sweeping_killbrick = None  # No sweeping killbrick in level 1
    elif level == 2:
        platforms = [
            (15, 430, 615, 10),
            (450, 400, 30, 40),
            (400, 340, 20, 20),
            (100, 0, 10, 100),
            (100, 210, 10, 30),
            (100, 375, 7.5, 60),
            (100, 230, 550, 10),
            (125, 210, 20, 20),
            (550, 175, 100, 10),
            (550, 100, 100, 10),
            (550, 50, 100, 10),
        ] + [(x-2, 320, 15, 15) for x in range(175, 350, 75)]
        killbricks = [
            (5, 420, 450, 10),
            (5, 0, 100, 10), 
            (100, 100, 10, 10),
            (100, 200, 10, 10),
            (110, 220, 20, 10)
        ]
        walls = [(-30, -20, 50, 1000), (620, -20, 50, 1000)]
        moving_platform = pygame.Rect(15, 400, 50, 10)
        sweeping_killbrick = pygame.Rect(200, 220, 50, 10)  # Only in level 2
    mario_x = mario_spawn_x
    mario_y = mario_spawn_y

# Load the initial stage
load_stage(level)

# Main game loop
running = True
while running:
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
        for platform in platforms + ([moving_platform] if moving_platform else []):
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

        if level == 2 and sweeping_killbrick:
            sweeping_killbrick.x += sweeping_speed * sweeping_direction
            if sweeping_killbrick.left <= 150 or sweeping_killbrick.right >= 610:
                sweeping_direction *= -1

        if sweeping_killbrick and mario_rect.colliderect(sweeping_killbrick):
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

    else:
        death_velocity += gravity
        mario_y += death_velocity

        mario_rect = pygame.Rect(mario_x, mario_y, 15, 25)

        if mario_y > HEIGHT + 100:
            pygame.time.delay(int(death_sound.get_length() * 1000))   
            running = False

    if level == 2 and moving_platform:
        moving_platform.y -= moving_speed
        if moving_platform.y < -moving_platform.height:
            moving_platform.y = HEIGHT

    if mario_y < 0:
        level += 1
        load_stage(level)
    # Drawing
    screen.fill((36, 40, 64))

    # Draw killbricks
    for kill in killbricks:
        pygame.draw.rect(screen, (255, 0, 0), kill)

    for platform in platforms:
        pygame.draw.rect(screen, (64, 64, 64), platform)

    if level == 2 and moving_platform:
        pygame.draw.rect(screen, (64, 64, 64), moving_platform)

    if sweeping_killbrick:
        pygame.draw.rect(screen, (255, 0, 0), sweeping_killbrick)

    if death_animation:
        moving_speed = 0

    for wall in walls:
        pygame.draw.rect(screen, (74, 74, 74), wall)

    pygame.draw.rect(screen, (66, 66, 66), (mario_x, mario_y, 15, 15))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 2.5, mario_y - 10, 10, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 2, mario_y + 15, 4, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 9, mario_y + 15, 4, 10))

    # Refresh the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
