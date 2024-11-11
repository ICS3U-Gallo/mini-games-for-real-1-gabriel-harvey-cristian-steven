import pygame
import time

pygame.init()

# Screen settings
WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Mario Tower Obstacle Course")
clock = pygame.time.Clock()

# Load sounds
death_sound = pygame.mixer.Sound("game_over.mp3")
pygame.mixer.music.load("escape.mp3")
pygame.mixer.music.play(-1)

# ---------------------------
# Initialize global variables

mario_x = 500
mario_y = 400
mario_speed = 10
velocity_y = 0
gravity = 5
ground = False
death = False
death_animation = False  # New variable to track death animation
death_velocity = 0       # Velocity during death animation

platforms = [
    (470, 430, 150, 10),
    (275, 400, 150, 10),
    (111, 369, 150, 10),
    (111, 309, 150, 10),
    (280, 270, 340, 10)
]

walls = [(-30, -20, 50, 1000), (620, -20, 50, 1000)]

killbricks = [
    (340, 380.5, 20, 20),
    (241, 289.9, 20, 20),
    (111, 289.9, 20, 20)
] + [(x, 255, 15, 15) for x in range(300, 600, 75)]

# ---------------------------
mario_rect = pygame.Rect(mario_x, mario_y, 15, 25)

# Initial collision check to see if Mario starts on a platform
for platform in platforms:
    platform_rect = pygame.Rect(platform)  # Hitbox for the obby
    if mario_rect.colliderect(platform_rect):
        ground = True  # If Mario is touching a platform, he's on it
        mario_y = platform_rect.top - mario_rect.height  # Mario is now on top of the platform
        break  # Stop checking once a collision is detected

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)

    # GAME STATE UPDATES
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

        if mario_y > HEIGHT + 30 and not death:
            pygame.mixer.music.stop()
            death_animation = True
            death_velocity = 0
            death_sound.play()
            print("Game Over!")
            time.sleep(0.5)

    else:
        death_velocity += gravity
        mario_y += death_velocity

        mario_rect = pygame.Rect(mario_x, mario_y, 15, 25)

        if mario_y > HEIGHT + 30:
            pygame.time.delay(int(death_sound.get_length() * 1000))   
            running = False  # End the game loop after death animation

    # DRAWING
    screen.fill((36, 40, 64))

    # Draw killbricks
    for kill in killbricks:
        pygame.draw.rect(screen, (255, 0, 0), kill)

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, (64, 64, 64), platform)

    # Draw towers walls
    for wall in walls:
        pygame.draw.rect(screen, (74, 74, 74), wall)

    # Draw Mario
    pygame.draw.rect(screen, (66, 66, 66), (mario_x, mario_y, 15, 15))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 2.5, mario_y - 10, 10, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 2, mario_y + 15, 4, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 9, mario_y + 15, 4, 10))

    # Example red killbricks
    for x in range(300, 600, 75):
        pygame.draw.rect(screen, (255, 0, 0), (x, 255, 15, 15))

    # Refresh the display
    pygame.display.flip()
    clock.tick(30)

# ---------------------------
pygame.quit()
