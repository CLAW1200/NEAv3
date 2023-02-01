
import math
import pygame
import random
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

class Goal:
    """
    A class to represent the goal.
    """
    def __init__(self, x, y, width, height):
        """
        Initialize the goal with its position and size.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (155, 255, 155)
        
    def draw(self, screen):
        """
        Draw the goal on the screen.
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def check_collision(self, projectile):
        """
        Check if the projectile has collided with the goal.
        """
        # Get the position of the projectile
        x, y = projectile.get_position()
        # Check if the projectile is within the goal
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
            return True
        else:
            return False

#Obstacle class that inherits from the Goal class
class Obstacle(Goal):
    """
    A class to represent an obstacle.
    """
    def __init__(self, x, y, width, height):
        """
        Initialize the obstacle with its position and size.
        """
        super().__init__(x, y, width, height)
        self.color = (255, 155, 155)

class Game:
    def __init__(self):
        # Initialize the game
        pygame.init()
        #set frame rate to 60 fps
        self.clock = pygame.time.Clock()
        # Set the screen size
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        # Create the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Set the background color
        self.bg_color = (32, 20, 22)
        # Set the constant for air resistance
        self.B2 = 0.00004
        # Set the initial position and velocity of the cannon
        self.cannon_x = 100
        self.cannon_y = self.SCREEN_HEIGHT - 100
        self.cannon_vx = 0
        self.cannon_vy = 10
        # Set the initial position and size of the target
        self.target_x = self.SCREEN_WIDTH - 100
        self.target_y = self.SCREEN_HEIGHT - 100
        self.target_width = 20
        self.target_height = 20
        # Set the initial position, velocity, mass, and drag coefficient of the projectile
        self.projectile_x = self.cannon_x
        self.projectile_y = self.cannon_y
        self.projectile_vx = self.cannon_vx
        self.projectile_vy = self.cannon_vy
        self.projectile_m = 2
        self.projectile_Cd = 0.47
        self.projectile_colour = (255, 255, 255)

        self.running = True
        self.game_over = False
        self.hit_target = False
        self.launched = False
        self.in_flight = False

        self.cannon = pygame.image.load("assets\cannonTube.png")
        

    def run(self):
        while self.running:
            # Create a Projectile object
            self.projectile = Projectile(self.projectile_x, self.projectile_y, self.projectile_vx, self.projectile_vy, self.projectile_m, self.projectile_Cd, self.B2, 9.81)
            # Set the initial game state
            while not self.game_over:
            # Handle events
                # Set the background color
                self.screen.fill(self.bg_color)
                # Draw the cannon with cannonTube.png at 10,10
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.angle = math.atan2(mouse_y - self.cannon_y, mouse_x - self.cannon_x)
                self.cannon = pygame.transform.rotate(self.cannon, math.degrees(-self.angle)-15)

                self.screen.blit(self.cannon, (self.cannon_x-30, self.cannon_y-40))
                
                # Draw the target
                self.target = Goal(self.target_x, self.target_y, self.target_width, self.target_height)
                self.target.draw(self.screen)

                #draw obstacles
                self.obstacle1 = Obstacle(400, 400, 100, 100)
                self.obstacle1.draw(self.screen)
                self.obstacle2 = Obstacle(200, 200, 100, 100)
                self.obstacle2.draw(self.screen)



                if self.launched:
                    self.power = ((mouse_x - self.cannon_x)**2 + (mouse_y - self.cannon_y)**2)**0.5 / 5
                    self.projectile.set_vx_vy(math.cos(-self.angle)*self.power, math.sin(-self.angle)*self.power)
                    self.launched = False
                    self.in_flight = True
                if self.in_flight:
                    self.projectile.update_position()
                    pygame.draw.circle(self.screen, (self.projectile_colour), (int(self.projectile.x), int(self.projectile.y)), 5)
                    if len(self.projectile.trajectory) > 1:
                        pygame.draw.lines(self.screen, self.projectile_colour, False, self.projectile.trajectory, 2)
                    if self.projectile.y > self.SCREEN_HEIGHT:
                        self.in_flight = False


                # Check if the projectile has hit the target
                if self.target.check_collision(self.projectile):
                    self.hit_target = True
                    print ("You hit the target!")
                    break
                if self.obstacle1.check_collision(self.projectile):
                    print ("You hit the obstacle!")
                    break
                if self.obstacle2.check_collision(self.projectile):
                    print ("You hit the obstacle!")
                    break
                # Check if the projectile has gone out of the screen
                if self.projectile.x < 0 or self.projectile.x > self.SCREEN_WIDTH or self.projectile.y > self.SCREEN_HEIGHT:
                    print ("You missed the target!")
                    break

                #write the velocity of the cannon on the screen
                font = pygame.font.SysFont("consolas", 20)
                #leave only 1 dp
                text = font.render(f"Cannon Velocity: {round(self.projectile.vx, 2)}, {round(self.projectile.vy, 2)}", True, (255, 255, 255))
                self.screen.blit(text, (10, 10))
                #write drag coefficient, mass, and air resistance on the screen
                text = font.render(f"Drag Coefficient: " + str(self.projectile_Cd) + ", Mass: " + str(self.projectile_m) + "Kg, Air Resistance: " + str(self.B2), True, (255, 255, 255))
                self.screen.blit(text, (10, 30))
                # Update the screen
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #if the user clicks the close button, end the game
                        self.running = False
                        self.game_over = True
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if not self.launched and not self.in_flight:
                                self.launched = True
                                self.projectile_colour = (random.randint(70, 255), random.randint(70, 255), random.randint(70, 255))
                            else:
                                pass
                    elif event.type == pygame.KEYDOWN:
                        #arrow keys control the velocity of the cannon
                        if event.key == pygame.K_UP:
                            self.projectile_vy += 1
                        elif event.key == pygame.K_DOWN:
                            self.projectile_vy -= 1
                        elif event.key == pygame.K_LEFT:
                            self.projectile_vx -= 1
                        elif event.key == pygame.K_RIGHT:
                            self.projectile_vx += 1
                        if event.key == pygame.K_SPACE:
                            if not self.launched and not self.in_flight:
                                launched = True
                                self.projectile_colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                            else:
                                pass
        pygame.quit()

game = Game()
game.run()