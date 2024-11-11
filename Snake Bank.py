import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (84, 214, 105)
GREY = (101, 107, 102)
RED = (156, 11, 11)

# Define the screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Set the display size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Define the snake block size and speed
BLOCK_SIZE = 20
SNAKE_SPEED = 15

# Load the background image and scale it to fit the screen
background_image = pygame.transform.scale(pygame.image.load("floorground.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the font for the score
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function to display the score
def Your_score(score):
    value = score_font.render("Cash collected: $" + str(score), True, WHITE)
    screen.blit(value, [0, 0])

# Function to draw the snake with a different color for the head
def our_snake(block_size, snake_list):
    for index, x in enumerate(snake_list):
        if index == len(snake_list) - 1:  # The head is the last element in the list
            pygame.draw.rect(screen, BLACK, [x[0], x[1], block_size, block_size])  # Head color
        else:
            pygame.draw.rect(screen, GREY, [x[0], x[1], block_size, block_size])  # Body color

# Function to display messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])

# Main function to run the game
def gameLoop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    # Snake list and initial length
    snake_List = []
    Length_of_snake = 1

    # Place the food at a random position
    foodx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while not game_over:

        while game_close:
            screen.blit(background_image, (0, 0))  # Draw the background image
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            # Check for player input after losing
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # Check if the snake hits the boundaries
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.blit(background_image, (0, 0))  # Draw the background image each frame

        # Draw the food
        pygame.draw.rect(screen, GREEN, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # Update the snake's position
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check if the snake collides with itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw the snake
        our_snake(BLOCK_SIZE, snake_List)

        # Display the score
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if the snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            Length_of_snake += 1

        # Set the speed of the game
        pygame.time.Clock().tick(SNAKE_SPEED)

    pygame.quit()

# Run the game loop
gameLoop()
