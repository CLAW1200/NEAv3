# Import the math module
import math
import pygame

class Projectile:
    """
    A class to simulate the flight of a projectile.
    """
    def __init__(self, x0, y0, vx0, vy0, mass, Cd, B2, gravity):
        """
        Initialize the projectile with its initial position, velocity, mass, drag
        coefficient, and the constant for air resistance.
        """
        self.x = x0
        self.y = y0
        self.vx = vx0
        self.vy = vy0
        self.m = mass
        self.Cd = Cd
        self.B2 = B2
        self.gravity = gravity
        # Set the color of the projectile's trajectory
        self.trace_color = (100, 0, 0)

        # Initialize the list of points in the projectile's trajectory
        self.trajectory = []
        
        # Set the time step
        self.dt = 0.05
                
        # Initialize the air resistance force
        self.Fx = -0.5 * Cd * B2 * vx0 * math.sqrt(vx0**2 + vy0**2)
        self.Fy = -0.5 * Cd * B2 * vy0 * math.sqrt(vx0**2 + vy0**2)
        
        # Initialize the acceleration of the projectile
        self.ax = self.Fx / self.m
        self.ay = self.Fy / self.m
        
        # Initialize the lists of positions
        self.xs = [self.x]
        self.ys = [self.y]
        
    def update_position(self):
        # Calculate the air resistance force
        self.Fx = -0.5 * self.Cd * self.B2 * self.vx * self.vx
        self.Fy = -0.5 * self.Cd * self.B2 * self.vy * self.vy + self.gravity  # Reverse the sign of the y-component of the velocity

        # Calculate the acceleration of the projectile
        self.ax = self.Fx / self.m
        self.ay = self.Fy / self.m

        # Update the position and velocity of the projectile
        self.x = self.x + self.vx * self.dt
        self.y = self.y - self.vy * self.dt # Reverse the sign of the y-coordinate
        self.vx = self.vx + self.ax * self.dt
        self.vy = self.vy - self.ay * self.dt  # Reverse the sign of the y-velocity

        # Add the new position of the projectile to the list of positions
        self.xs.append(self.x)
        self.ys.append(self.y)

        # Add the current position of the projectile to the list of points in its trajectory
        self.trajectory.append((self.x, self.y))


    def set_vx_vy(self, vx, vy):
        """
    Set the velocity of the projectile.
        """
        self.vx = vx
        self.vy = vy
        
    def get_position(self):
        """
        Return the current position of the projectile.
        """
        return self.x, self.y
    
    def get_velocity(self):
        """
        Return the current velocity of the projectile.
        """
        return self.vx, self.vy
    

# Initialize the game
pygame.init()
#set frame rate to 60 fps
clock = pygame.time.Clock()
# Set the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the background color
bg_color = (23, 5, 52)

# Set the constant for air resistance
B2 = 0.00004

# Set the initial position and velocity of the cannon
cannon_x = 100
cannon_y = SCREEN_HEIGHT - 100
cannon_vx = 0
cannon_vy = 10

# Set the initial position and size of the target
target_x = SCREEN_WIDTH - 100
target_y = SCREEN_HEIGHT - 100
target_size = 10

# Set the initial position and size of the cannon ball
cannon_ball_x = cannon_x + 50
cannon_ball_y = cannon_y - 50
cannon_ball_size = 10

# Set the mass of the cannon ball
cannon_ball_mass = 1

# Set the drag coefficient of the cannon ball
cannon_ball_Cd = 0.45

# Set the initial velocity of the cannon ball
cannon_ball_vx = 0
cannon_ball_vy = 0

# Set the acceleration due to gravity
gravity = 9.81

# Create the cannon ball
cannon_ball = Projectile(cannon_ball_x, cannon_ball_y, cannon_ball_vx, cannon_ball_vy, cannon_ball_mass, cannon_ball_Cd, B2, gravity)

# Set the initial value of the game over flag
game_over = False

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        # Quit the game if the player closes the window
        if event.type == pygame.QUIT:
            game_over = True

    # Get the current position of the mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate the angle of the cannon relative to the horizontal
    cannon_angle = math.atan2(cannon_y - mouse_y, cannon_x - mouse_x)

    # Set the initial velocity of the cannon ball based on the distance between the cannon and the mouse
    cannon_ball_vx = (cannon_x - mouse_x) / 5
    cannon_ball_vy = (cannon_y - mouse_y) / 5

    # Set the velocity of the cannon ball
    cannon_ball.set_vx_vy(cannon_ball_vx, cannon_ball_vy)

    # Draw the screen
    screen.fill(bg_color)
    
    # Rotate the cannon
    cannon_surface = pygame.Surface((100, 20))
    cannon_surface.fill((0, 0, 0))
    rotated_cannon = pygame.transform.rotate(cannon_surface, -cannon_angle)
    rect = rotated_cannon.get_rect()
    rect.center = (cannon_x, cannon_y)
    screen.blit(rotated_cannon, rect)
    
    # Draw the target
    pygame.draw.circle(screen, (255, 255, 255), (target_x, target_y), target_size)
    
    # Draw the cannon ball
    cannon_ball_x, cannon_ball_y = cannon_ball.get_position()
    pygame.draw.circle(screen, (255, 255, 255), (cannon_ball_x, cannon_ball_y), cannon_ball_size)
    
    # Update the position of the cannon ball
    cannon_ball.update_position()
    
    # Check if the cannon ball has hit the target
    if (cannon_ball_x - target_x)**2 + (cannon_ball_y - target_y)**2 <= target_size**2:
        game_over = True
        
    # Update the screen
    pygame.display.update()
    
    # Set the frame rate to 60 fps
    clock.tick(60)

# Print a message when the game is over
print("You hit the target!")
