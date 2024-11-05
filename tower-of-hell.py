import pygame


pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

mario_x = 500
mario_y = 400
mario_speed = 5
height = 0
gravity = 5
ground = True
death = False
platforms = ((470, 430, 150, 10))
# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mario_x -= mario_speed
    if keys[pygame.K_RIGHT]:
        mario_x += mario_speed
    if keys[pygame.K_SPACE]:
        velocity_y = -10
        on_ground = False    

    height += gravity
    mario_y += height

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((36, 40, 64))

    # Mario guy thing idk lol
    pygame.draw.rect(screen, (66, 66, 66), (mario_x, mario_y, 15, 15))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x+2.5, mario_y-10, 10, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x+2, mario_y+15, 4, 10))
    pygame.draw.rect(screen, (247, 232, 119), (mario_x+9, mario_y+15, 4, 10))

    # Tower walls
    pygame.draw.rect(screen, (74, 74, 74), (-30, -20, 50, 1000))
    pygame.draw.rect(screen, (74, 74, 74), (620, -20, 50, 1000))

    # obby
    pygame.draw.rect(screen, (113, 122, 60), (470, 430, 150, 10))

    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
