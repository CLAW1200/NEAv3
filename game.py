import math # Import the math module
import pygame # Import the pygame module
import random # Import the random module
class Projectile: # Projectile class
    """
    A class to simulate the flight of a projectile.
    """
    def __init__(self, x0, y0, vx0, vy0, mass, Cd, B2, gravity):
        """
        Initialize the projectile with its initial position, velocity, mass, drag
        coefficient, and the constant for air resistance.
        """
        self.x = x0 # Initial x-position
        self.y = y0 # Initial y-position
        self.vx = vx0 # Initial x-velocity
        self.vy = vy0 # Initial y-velocity
        self.m = mass # Mass of the projectile
        self.Cd = Cd # Drag coefficient
        self.B2 = B2 # Constant for air resistance
        self.gravity = gravity # Acceleration due to gravity
        # Set the color of the projectile's trajectory
        self.trace_color = (100, 0, 0) # A line that follows the projectile path

        # Initialize the list of points in the projectile's trajectory
        self.trajectory = [] # A list of points that follow the projectile path
        
        # Set the time step
        self.dt = 0.05 # Time step is how often the position of the projectile is updated in the simulation (not the same as the frame rate)
                
        # Initialize the air resistance force
        self.Fx = -0.5 * Cd * B2 * vx0 * math.sqrt(vx0**2 + vy0**2) # The x-component of the air resistance force
        self.Fy = -0.5 * Cd * B2 * vy0 * math.sqrt(vx0**2 + vy0**2) # The y-component of the air resistance force
        
        # Initialize the acceleration of the projectile
        self.ax = self.Fx / self.m # The x-component of the acceleration of the projectile
        self.ay = self.Fy / self.m # The y-component of the acceleration of the projectile
        
        # Initialize the lists of positions
        self.xs = [self.x] # A list of the x-positions of the projectile
        self.ys = [self.y] # A list of the y-positions of the projectile
        
    def update_position(self):
        # Calculate the air resistance force
        self.Fx = -0.5 * self.Cd * self.B2 * self.vx * self.vx # A calculation of the x-component of the air resistance force
        self.Fy = -0.5 * self.Cd * self.B2 * self.vy * self.vy + self.gravity  # Reverse the sign of the y-component of the velocity so that the y-axis points up and is displayed correctly on the screen
        
        # Calculate the acceleration of the projectile
        self.ax = self.Fx / self.m # A calculation of the x-component of the acceleration of the projectile
        self.ay = self.Fy / self.m # A calculation of the y-component of the acceleration of the projectile

        # Update the position and velocity of the projectile
        self.x = self.x + self.vx * self.dt # A calculation of the new x-position of the projectile
        self.y = self.y - self.vy * self.dt # Reverse the sign of the y-coordinate (same reason as above)
        self.vx = self.vx + self.ax * self.dt # A calculation of the new x-velocity of the projectile
        self.vy = self.vy - self.ay * self.dt  # Reverse the sign of the y-velocity (same reason as above)

        # Add the new position of the projectile to the list of positions
        self.xs.append(self.x) # Add the new x-position of the projectile to the list of x-positions
        self.ys.append(self.y) # Add the new y-position of the projectile to the list of y-positions
        # Add the current position of the projectile to the list of points in its trajectory
        self.trajectory.append((self.x, self.y)) # Add the current position of the projectile to the list of points in its trajectory


    def set_vx_vy(self, vx, vy):
        """
        A method to set the velocity of the projectile.
        """
        self.vx = vx # Set the x-velocity of the projectile to the value of the parameter vx
        self.vy = vy # Set the y-velocity of the projectile to the value of the parameter vy
        
    def get_position(self):
        """
        A method to return the current position of the projectile.
        """
        return self.x, self.y # Return the current position of the projectile as a tuple
    
    def get_velocity(self):
        """
        A method to return the current velocity of the projectile.
        """
        return self.vx, self.vy # Return the current velocity of the projectile as a tuple

class Goal:
    """
    A class to represent the goal.
    """
    def __init__(self, x, y, width, height):
        """
        Initialize the goal with its position and size.
        """
        self.x = x # Set the x-position of the goal to the value of the parameter x
        self.y = y # Set the y-position of the goal to the value of the parameter y
        self.width = width # Set the width of the goal to the value of the parameter width
        self.height = height # Set the height of the goal to the value of the parameter height
        self.color = (155, 255, 155) # Set the color of the goal to a light green (pre defined color and not a parameter)
        
    def draw(self, screen):
        """
        A method to draw the goal on the screen.
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height)) # Draw the goal on the screen as a rectangle with the color, position, and size specified by the attributes of the goal object

    def check_collision(self, projectile):
        """
        A method to check if the projectile has collided with the goal.
        """
        x, y = projectile.get_position() # Get the position of the projectile
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height: # Check if the x-position of the projectile is between the left and right sides of the goal and if the y-position of the projectile is between the top and bottom of the goal
            return True # Return True if the projectile has collided with the goal
        else:
            return False # Return False if the projectile has not collided with the goal


class Obstacle(Goal):
    """
    A class to represent an obstacle that inherits from the Goal class.
    """
    def __init__(self, x, y, width, height): # The constructor of the Obstacle class
        """
        Initialize the obstacle with its position and size.
        """
        super().__init__(x, y, width, height) # Call the constructor of the Goal class
        self.color = (255, 155, 155) # Set the color of the obstacle to a light red (pre defined color and not a parameter)


class Game: # A class to represent the game loop
    def run(self): # A method to run the game loop
        pygame.init() # Initialize pygame
        clock = pygame.time.Clock() # Set frame rate to 60 fps
        SCREEN_WIDTH = 800 # Set the width of the screen
        SCREEN_HEIGHT = 600 # Set the height of the screen

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Create a screen with the specified width and height
        bg_color = (32, 20, 22) # Set the background color of the screen to a dark red (pre defined color and not a parameter)
        B2 = 0.00004 # Set the drag coefficient of the projectile to 0.00004 (pre defined value and not a parameter)
        cannon_x = 100 # Set the initial x-position of the cannon in pixels
        cannon_y = SCREEN_HEIGHT - 100 # Set the initial y-position of the cannon in pixels
        cannon_vx = 0 # Set the initial x-velocity of the cannon in meters per second
        cannon_vy = 10 # Set the initial y-velocity of the cannon in meters per second
        target_x = SCREEN_WIDTH - 100 # Set the initial x-position of the target in pixels
        target_y = SCREEN_HEIGHT - 100 # Set the initial y-position of the target in pixels
        target_width = 20 # Set the width of the target in pixels
        target_height = 20 # Set the height of the target in pixels
        # Set the initial position, velocity, mass, and drag coefficient of the projectile
        projectile_x = cannon_x # Set the initial x-position of the projectile to the x-position of the cannon
        projectile_y = cannon_y # Set the initial y-position of the projectile to the y-position of the cannon
        projectile_vx = cannon_vx # Set the initial x-velocity of the projectile to the x-velocity of the cannon
        projectile_vy = cannon_vy # Set the initial y-velocity of the projectile to the y-velocity of the cannon
        projectile_m = 2 # Set the mass of the projectile to 2 kilograms
        projectile_Cd = 0.47 # Set the drag coefficient of the projectile to 0.47
        projectile_colour = (255, 255, 255) # Set the color of the projectile to white

        running = True # A boolean variable to indicate if the game is running

        while running: # A loop to run the game while th boolean variable is True
            projectile = Projectile(projectile_x, projectile_y, projectile_vx, projectile_vy, projectile_m, projectile_Cd, B2, 9.81) # Create a projectile object with the specified position, velocity, mass, drag coefficient, and acceleration due to gravity
            game_over = False # A boolean variable to indicate if the game is over
            hit_target = False # A boolean variable to indicate if the projectile has hit the target
            launched = False # A boolean variable to indicate if the projectile has been launched
            in_flight = False # A boolean variable to indicate if the projectile is in flight
            while not game_over: # A loop to run the game while the boolean variable is False
                """
                This section of the code is executed once per frame and will handle any events that occur
                """
                screen.fill(bg_color) # Fill the screen with the background color
                cannon = pygame.image.load("assets\cannonTube.png") # Load the cannon image from the assets folder
                mouse_x, mouse_y = pygame.mouse.get_pos() # Get the position of the mouse in pixels inside the window
                angle = math.atan2(mouse_y - cannon_y, mouse_x - cannon_x) # Calculate the angle between the cannon and the mouse
                cannon = pygame.transform.rotate(cannon, math.degrees(-angle)-15) # Rotate the cannon image to the angle between the cannon and the mouse
                screen.blit(cannon, (cannon_x-30, cannon_y-40)) # Draw the cannon image on the screen
                
                target = Goal(target_x, target_y, target_width, target_height) # Create a target object with the specified position and size
                target.draw(screen) # Draw the target on the screen

                obstacle1 = Obstacle(400, 400, 100, 100) # Create an obstacle object with the specified position and size
                obstacle1.draw(screen) # Draw the obstacle on the screen
                obstacle2 = Obstacle(200, 200, 100, 100) # Repeat the process for the second obstacle
                obstacle2.draw(screen) # Repeat the process for the second obstacle

                if launched: # If the projectile has been launched
                    power = ((mouse_x - cannon_x)**2 + (mouse_y - cannon_y)**2)**0.5 / 5 # Calculate the power of the projectile based on the distance between the cannon and the mouse
                    projectile.set_vx_vy(math.cos(-angle)*power, math.sin(-angle)*power) # Set the x-velocity and y-velocity of the projectile based on the power and angle between the cannon and the mouse
                    launched = False # Set the boolean variable to False to indicate that the projectile has been launched
                    in_flight = True # Set the boolean variable to True to indicate that the projectile is in flight
                if in_flight: # If the projectile is in flight
                    projectile.update_position() # Call the method to update the position of the projectile
                    pygame.draw.circle(screen, (projectile_colour), (int(projectile.x), int(projectile.y)), 5) # Draw the projectile on the screen
                    if len(projectile.trajectory) > 1: # If the projectile has a trajectory
                        pygame.draw.lines(screen, projectile_colour, False, projectile.trajectory, 2) # Draw the trajectory of the projectile on the screen
                    if projectile.y > SCREEN_HEIGHT: # If the projectile has gone out of the screen
                        in_flight = False # Set the boolean variable to False to indicate that the projectile is no longer in flight


                if target.check_collision(projectile): # Call the method to check if the projectile has hit the target
                    hit_target = True # Set the boolean variable to True to indicate that the projectile has hit the target
                    print ("You hit the target!") # Print a message to the console
                    break
                if obstacle1.check_collision(projectile): # Call the method to check if the projectile has hit the first obstacle
                    print ("You hit the obstacle!") # Same as above
                    break
                if obstacle2.check_collision(projectile): 
                    print ("You hit the obstacle!")
                    break
                if projectile.x < 0 or projectile.x > SCREEN_WIDTH or projectile.y > SCREEN_HEIGHT: # If the projectile has gone out of the screen 
                    print ("You missed the target!")
                    break

                font = pygame.font.SysFont("consolas", 20) # Set the font and size of the text that will be displayed on the screen
                text = font.render(f"Cannon Velocity: {round(projectile.vx, 2)}, {round(projectile.vy, 2)}", True, (255, 255, 255)) # Write the x-velocity and y-velocity of the cannon on the screen and round the values to 2 decimal places. Text is white
                screen.blit(text, (10, 10)) # Draw the text on the screen
                text = font.render(f"Drag Coefficient: " + str(projectile_Cd) + ", Mass: " + str(projectile_m) + "Kg, Air Resistance: " + str(B2), True, (255, 255, 255)) # Write the drag coefficient, mass, and air resistance of the projectile on the screen. Text is white
                screen.blit(text, (10, 30)) # Draw the text on the screen
                pygame.display.flip() # Update the screen
                for event in pygame.event.get(): # Get all the events that occur
                    if event.type == pygame.QUIT: # If the user clicks the close button, end the game
                        running = False # Set the boolean variable to False to indicate that the game is over
                        game_over = True # Set the boolean variable to True to indicate that the game is over
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN: # If the user clicks the mouse
                        if event.button == 1: # If the user clicks the left mouse button
                            if not launched and not in_flight: # If the projectile has not been launched and is not in flight
                                launched = True # Set the boolean variable to True to indicate that the projectile has been launched
                                projectile_colour = (random.randint(70, 255), random.randint(70, 255), random.randint(70, 255)) # Set the colour of the projectile tracer to a random colour
                            else: # If the projectile has been launched or is in flight
                                pass # Do nothing
                    elif event.type == pygame.KEYDOWN: # If the user presses a key
                        #arrow keys control the velocity of the cannon
                        if event.key == pygame.K_UP: # If the user presses the up arrow key
                            projectile_vy += 1 # Increase the y-velocity of the cannon by 1
                        elif event.key == pygame.K_DOWN: # If the user presses the down arrow key
                            projectile_vy -= 1 # Decrease the y-velocity of the cannon by 1
                        elif event.key == pygame.K_LEFT: # If the user presses the left arrow key
                            projectile_vx -= 1 # Decrease the x-velocity of the cannon by 1
                        elif event.key == pygame.K_RIGHT: # If the user presses the right arrow key
                            projectile_vx += 1 # Increase the x-velocity of the cannon by 1
                        if event.key == pygame.K_SPACE: # If the user presses the space bar
                            if not launched and not in_flight: # If the projectile has not been launched and is not in flight
                                launched = True # Set the boolean variable to True to indicate that the projectile has been launched
                                projectile_colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) # Set the colour of the projectile tracer to a random colour
                            else: # If the projectile has been launched or is in flight
                                pass # Do nothing
        pygame.quit() # Quit the game

