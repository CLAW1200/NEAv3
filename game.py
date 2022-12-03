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
        self.dt = 0.03
        
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
cannon_vx = 10
cannon_vy = 10

# Set the initial position and size of the target
target_x = SCREEN_WIDTH - 100
target_y = SCREEN_HEIGHT - 100
target_width = 20
target_height = 20

# Set the initial position, velocity, mass, and drag coefficient of the projectile
projectile_x = cannon_x
projectile_y = cannon_y
projectile_vx = cannon_vx
projectile_vy = cannon_vy
projectile_m = 10
projectile_Cd = 0.47

running = True
while running:
    # Create a Projectile object
    projectile = Projectile(projectile_x, projectile_y, projectile_vx, projectile_vy, projectile_m, projectile_Cd, B2, 9.81)

    # Set the initial game state
    game_over = False
    hit_target = False
    launched = False

    while not game_over:
    # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #if the user clicks the close button, end the game
                running = False
                game_over = True
                break
            elif event.type == pygame.KEYDOWN:
                #arrow keys control the velocity of the cannon
                if event.key == pygame.K_UP:
                    projectile_vy += 1
                elif event.key == pygame.K_DOWN:
                    projectile_vy -= 1
                elif event.key == pygame.K_LEFT:
                    projectile_vx -= 1
                elif event.key == pygame.K_RIGHT:
                    projectile_vx += 1
                if event.key == pygame.K_SPACE:
                    if not launched:
                        launched = True
                        projectile.set_vx_vy(projectile_vx, projectile_vy)
                    else:
                        pass

        # Update the position and velocity of the projectile
        if launched:  # NEW
            projectile.update_position()

        # Check if the projectile has hit the target
        if projectile.x > target_x and projectile.x < target_x + target_width and projectile.y > target_y and projectile.y < target_y + target_height:
            hit_target = True
            game_over = False
            print ("You hit the target!")
            break
        # Check if the projectile has gone out of the screen
        if projectile.x < 0 or projectile.x > SCREEN_WIDTH or projectile.y > SCREEN_HEIGHT:
            game_over = False
            print ("You missed the target!")
            break
        # Set the background color
        screen.fill(bg_color)

        # Draw the cannon
        pygame.draw.rect(screen, (0, 0, 0), (cannon_x, cannon_y, 20, 20))

        # Draw the target
        pygame.draw.rect(screen, (0, 0, 0), (target_x, target_y, target_width, target_height))

        # Draw the projectile
        pos = projectile.get_position()
        pygame.draw.circle(screen, (255, 0, 0), pos, 4)

        # Draw the projectile's trajectory on the screen
        if len(projectile.trajectory) > 1:
            pygame.draw.lines(screen, projectile.trace_color, False, projectile.trajectory, 2)

        #write the velocity of the cannon on the screen
        font = pygame.font.SysFont("consolas", 20)
        text = font.render(f"Cannon Velocity: " + str(projectile_vx) + ", " + str(projectile_vy), True, (255, 255, 255))
        screen.blit(text, (10, 10))
        #write drag coefficient, mass, and air resistance on the screen
        text = font.render(f"Drag Coefficient: " + str(projectile_Cd) + ", Mass: " + str(projectile_m) + "Kg, Air Resistance: " + str(B2), True, (255, 255, 255))
        screen.blit(text, (10, 30))
        # Update the screen
        pygame.display.flip()
pygame.quit()