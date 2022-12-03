import sys
import pygame

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption('Bouncing Ball')

# Set the color of the ball
color = (255, 0, 0)

# Set the initial position and velocity of the ball
x_pos = 50
y_pos = 50
x_vel = 3
y_vel = 2

# Set the radius of the ball
radius = 20

# Set the acceleration due to gravity
gravity = 0.3

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Run the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the velocity of the ball
    y_vel += gravity

    # Update the position of the ball
    x_pos += x_vel
    y_pos += y_vel

    # Check if the ball has hit the edge of the screen
    if x_pos + radius >= screen_width or x_pos - radius <= 0:
        x_vel = -x_vel
    if y_pos + radius >= screen_height or y_pos - radius <= 0:
        y_vel = -y_vel

    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    # Draw the ball on the screen
    pygame.draw.circle(screen, color, (x_pos, y_pos), radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)
