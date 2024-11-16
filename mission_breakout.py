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
winner_sound = pygame.mixer.Sound("winner.mp3")
run = pygame.mixer.Sound("getout.mp3")
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
level = 1 # CHANGE THIS TO MOD WHAT LEVEL YOU WANT TO GO TO!!!!!
sweeping_killbrick = None
sweeping_speed = 10
sweeping_direction = 1 
moving_platform = None
moving_speed = 5
beat_blocks = []
beat_interval = 1000 
last_toggle_time = pygame.time.get_ticks()
beat_block_visible = True
font = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 12)

def load_stage(level):
    global platforms, killbricks, walls, mario_y, moving_platform, sweeping_killbrick, beat_blocks, mario_x
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
        moving_platform = None
        sweeping_killbrick = None
        beat_blocks = []
        mario_x = mario_spawn_x
        mario_y = mario_spawn_y
        
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
        mario_x = mario_spawn_x
        mario_y = mario_spawn_y
        walls = [(-30, -20, 50, 1000), (620, -20, 50, 1000)]
        moving_platform = pygame.Rect(15, 400, 50, 10)
        sweeping_killbrick = pygame.Rect(160, 220, 50, 10)
        beat_blocks = []
    elif level == 3:
        platforms = [
            (15, 430, 615, 10),
            (300, 380, 100, 10),
            (400, 380, 15, 50),
            (410, 400, 15, 30),
            (420, 420, 15, 10),
            (20, 320, 110, 10),
            (250, 240, 200, 10),
            (440, 240, 10, 55),
            (450, 260, 10, 35),
            (460, 275, 10, 15),
            (510, 275, 10, 15),
            (520, 255, 10, 35),
            (530, 240, 10, 45),
            (455, 285, 85, 10),
            (540, 240, 95, 10),
            (600, 120, 20, 10),
            (360, 120, 20, 10),
            (240, 120, 20, 10),
            (120, 120, 20, 10)
        ]
        killbricks = [
            (20, 420, 380, 10),
            (350, 370, 15, 15),
            (470, 405, 10, 30),
            (600, 230, 30, 10),
            (300, 120, 20, 10),
        ]
        moving_platform = None
        sweeping_killbrick = pygame.Rect(500, 190, 10, 50)
        beat_blocks = [
            pygame.Rect(170, 360, 100, 10),
            pygame.Rect(170, 270, 20, 10),
            pygame.Rect(600, 180, 20, 10),
            pygame.Rect(520, 120, 20, 10),
            pygame.Rect(440, 120, 20, 10),
            pygame.Rect(140, 120, 100, 10),
            pygame.Rect(90, 80, 10, 10),
            pygame.Rect(50, 30, 10, 10)
        ]
        mario_x = mario_spawn_x
        mario_y = mario_spawn_y
    elif level == 4:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("getout.mp3")
        pygame.mixer.music.play(-1)
        platforms = [
            (5, 430, 400, 10),
            (245, 160, 90, 50),
            (245, 200, 40, 100),
            (275, 270, 60, 30),
            (275, 270, 60, 30),
            (295, 220, 40, 50),
            (345, 160, 90, 50),
            (345, 200, 40, 100),
            (375, 270, 60, 30),
            (395, 220, 40, 50),
            (405, 430, 10, 200),
            (465, 440, 5, 5),
            (535, 430, 200, 10),
        ]
        killbricks = [
            (235, 150, 100, 10),
            (235, 300, 100, 10),
            (235, 150, 10, 150),
            (285, 210, 50, 10),
            (285, 220, 10, 50),
            (335, 150, 100, 10),
            (335, 300, 110, 10),
            (335, 150, 10, 150),
            (435, 150, 10, 150),
            (385, 210, 50, 10),
            (385, 220, 10, 50)
        ] + [(x, 415, 25, 25) for x in range(100, 400, 80)]
        mario_x = mario_spawn_x-450
        mario_y = mario_spawn_y
        sweeping_killbrick = None
        beat_blocks = []
    walls = [(-30, -20, 50, 1000), (620, -20, 50, 1000)]



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
            velocity_y = -25
            ground = False    

        if not ground:
            velocity_y += gravity

        mario_y += velocity_y

        mario_rect = pygame.Rect(mario_x, mario_y, 15, 25)
        current_time = pygame.time.get_ticks()
        if current_time - last_toggle_time > beat_interval:
            beat_block_visible = not beat_block_visible
            last_toggle_time = current_time

        ground = False  # Assume Mario is in the air
        # i am also including platforms and visible beat blocks in the collision check
        for platform in platforms + ([moving_platform] if moving_platform else []) + (
                [pygame.Rect(bb) for bb in beat_blocks] if beat_block_visible else []):
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

        if level == 3 and sweeping_killbrick:
            sweeping_killbrick.x += sweeping_speed * sweeping_direction
            if sweeping_killbrick.left <= 250 or sweeping_killbrick.right >= 615:
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

    if level == 4:
        car_rect = pygame.Rect(545, 390, 45, 25)  
        if mario_rect.colliderect(car_rect):
            winner_sound.play() 
            mario_x = 0
            mario_y = 0
            velocity_y = 0
            pygame.time.delay(3000)
            running = False

    # Drawing
    screen.fill((36, 40, 64))

    for kill in killbricks:
        pygame.draw.rect(screen, (255, 0, 0), kill)

    
    if level == 4:
        text = font2.render("don't fail this lol", True, (255, 255, 255))
        screen.blit(text, (440, 460))  # Center the text


    if level == 1:
        text = font.render("Dodge the traps and get to your getaway vehicle.", True, (255, 255, 255))
        screen.blit(text, (60, 430))  # Center the text

    for platform in platforms:
        pygame.draw.rect(screen, (64, 64, 64), platform)

    if level == 2 and moving_platform:
        pygame.draw.rect(screen, (64, 64, 64), moving_platform)

    if sweeping_killbrick:
        pygame.draw.rect(screen, (255, 0, 0), sweeping_killbrick)

    if mario_y < 0:
        level += 1
        load_stage(level)

    if death_animation:
        moving_speed = 0

    for wall in walls:
        pygame.draw.rect(screen, (74, 74, 74), wall)

    if beat_block_visible:
        for beat_block in beat_blocks:
            pygame.draw.rect(screen, (90,90,90), beat_block)

    if level == 4:
        pygame.draw.rect(screen, (66, 66, 66), (545, 390, 45, 25))
        pygame.draw.rect(screen, (100,100,100), (590, 400, 15, 15))
        pygame.draw.circle(screen, (24, 24, 24), (590, 420), 7.5)
        pygame.draw.circle(screen, (24, 24, 24), (550, 420), 7.5)

    pygame.draw.rect(screen, (66, 66, 66), (mario_x, mario_y, 15, 15))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 2.5, mario_y - 10, 10, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 2, mario_y + 15, 4, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x + 9, mario_y + 15, 4, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
