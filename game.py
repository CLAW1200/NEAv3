import pygame
import random

WIDTH = 800
HEIGHT = 600

BALL_RADIUS = 20
BALL_COLOR = (255, 255, 255)

BALL_SPEED = 5

class Ball:
    def __init__(self):
        self.x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
        self.y = random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED
        self.radius = BALL_RADIUS
        self.color = BALL_COLOR

    def update(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt

        if self.x + self.radius >= WIDTH or self.x - self.radius <= 0:
            self.speed_x = -self.speed_x
        if self.y + self.radius >= HEIGHT or self.y - self.radius <= 0:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def game_loop(screen):
    clock = pygame.time.Clock()
    ball = Ball()

    running = True
    while running:
        dt = clock.tick(10) / 10  # Amount of seconds between each frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball.update(dt)
        screen.fill((0, 0, 0))
        ball.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_loop(screen)
    pygame.quit()
