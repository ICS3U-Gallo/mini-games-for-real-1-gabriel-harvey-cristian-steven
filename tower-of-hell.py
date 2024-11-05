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
death = False
# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)

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

    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
