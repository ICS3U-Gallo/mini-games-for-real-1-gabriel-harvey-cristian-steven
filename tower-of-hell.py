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
mario_speed = 10
height2 = 0
gravity = 5
ground = False
death = False
platforms = [(470, 430, 150, 10), (275, 400, 150, 10)]
walls = [(-30, -20, 50, 1000), (620, -20, 50, 1000)] 
# ---------------------------
mario_rect = pygame.Rect(mario_x, mario_y, 15, 25)
for platform in platforms:
    platform_rect = pygame.Rect(platform) # Hitbox for the obby
    if mario_rect.colliderect(platform_rect):
        ground = True # If mario is touching a platform he's on it
        mario_y = platform_rect.top - mario_rect.height # mario is now on the top of a platform depending on jump or not
        break # stop the code once it detects that 

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
    if keys[pygame.K_SPACE] and ground:
        height2 = -25
        ground = False    

    if not ground:
        height2 += gravity

    mario_y += height2

    mario_rect = pygame.Rect(mario_x, mario_y, 15, 25)

    ground = False  # assume Mario is in the air
    for platform in platforms:
        platform_rect = pygame.Rect(platform)
        if mario_rect.colliderect(platform_rect) and height2 >= 0:
            mario_y = platform_rect.top - mario_rect.height 
            height2 = 0
            ground = True
            break

    for wall in walls:
        wall_rect = pygame.Rect(wall)
        if mario_rect.colliderect(wall_rect):
            if mario_rect.right > wall_rect.left and mario_rect.left < wall_rect.left:
                 mario_x = wall_rect.left - mario_rect.width
            elif mario_rect.left < wall_rect.right and mario_rect.right > wall_rect.right:
                 mario_x = wall_rect.right


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
    for platform in platforms:
        pygame.draw.rect(screen, (113, 122, 60), platform)
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
