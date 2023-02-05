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
        self.bounceAbsorption = 2 # The amount of energy absorbed when the projectile bounces off the ground (multiplier)
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

    def set_position(self, x, y):
        """
        A method to set the position of the projectile.
        """
        self.x = x # Set the x-position of the projectile to the value of the parameter x
        self.y = y # Set the y-position of the projectile to the value of the parameter y
        
        
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

    def bounce(self, absorption):
        """
        A method to bounce the projectile off the ground.
        """
        self.vy = -self.vy / absorption # Reverse the sign of the y-velocity and reduce it by the absorption multiplier


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
    
    def get_coordinates(self):
        """
        A method to return the coordinates of the obstacle.
        """
        return self.x, self.y, self.x + self.width, self.y + self.height # Return the coordinates of the obstacle as a tuple

    def check_collision(self, projectile):
        """
        A method to check if the projectile has collided with the goal.
        """
        x, y = projectile.get_position()
        x1, y1, x2, y2 = self.get_coordinates()
        #if projectile is inside the obstacle move it to the surface of the obstacle
        if x > x1 and x < x2 and y > y1 and y < y2:
            vx, vy = projectile.get_velocity()
            if x < x1 + 5:
                x = x1
                vx = -vx
            elif x > x2 - 5:
                x = x2
                vx = -vx
            elif y < y1 + 5:
                y = y1
                vy = -vy
            elif y > y2 - 5:
                y = y2
                vy = -vy
            projectile.set_vx_vy(vx, vy)
            projectile.x = x
            projectile.y = y
            return True
        else:
            return False

class Cannon:
    def __init__(self, x, y):
        """
        Initialize the cannon with its position and size.
        """
        self.x = x
        self.y = y
        self.cannon_image = pygame.image.load("assets\cannonTube.png") # Load the cannon image from the assets folder
        self.power = 0 # Create a variable to store the power of the cannon

    def rot_center(self, angle):
        """
        A method to rotate the cannon image.
        """
        orig_rect = self.cannon_image.get_rect()
        rot_image = pygame.transform.rotate(self.cannon_image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image


class Game: # A class to represent the game loop
    def __init__(self):
        pygame.init() # Initialize pygame
        pygame.time.Clock() # Set frame rate to 60 fps
        self.SCREEN_WIDTH = 1400 # Set the width of the screen
        self.SCREEN_HEIGHT = 600 # Set the height of the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT)) # Create a screen with the specified width and height
        self.bg_color = (32, 20, 22) # Set the background color of the screen to a dark red (pre defined color and not a parameter)
        self.B2 = 0.00004 # Set the drag coefficient of the projectile to 0.00004 (pre defined value and not a parameter)
        self.cannon_x = 100 # Set the initial x-position of the cannon in pixels
        self.cannon_y = self.SCREEN_HEIGHT - 100 # Set the initial y-position of the cannon in pixels
        self.cannon_vx = 0 # Set the initial x-velocity of the cannon in meters per second
        self.cannon_vy = 0 # Set the initial y-velocity of the cannon in meters per second
        self.target_x = self.SCREEN_WIDTH - 100 # Set the initial x-position of the target in pixels
        self.target_y = self.SCREEN_HEIGHT - 100 # Set the initial y-position of the target in pixels
        self.target_width = 20 # Set the width of the target in pixels
        self.target_height = 20 # Set the height of the target in pixels
        self.projectile_x = self.cannon_x # Set the initial x-position of the projectile to the x-position of the cannon
        self.projectile_y = self.cannon_y # Set the initial y-position of the projectile to the y-position of the cannon
        self.projectile_vx = self.cannon_vx # Set the initial x-velocity of the projectile to the x-velocity of the cannon
        self.projectile_vy = self.cannon_vy # Set the initial y-velocity of the projectile to the y-velocity of the cannon
        self.projectile_m = 2 # Set the mass of the projectile to 2 kilograms
        self.projectile_Cd = 0.47 # Set the drag coefficient of the projectile to 0.47
        self.projectile_colour = (255, 255, 255) # Set the color of the projectile to white
        self.levelCounter = 20 # Create a variable to store the current level
        self.obstacleList = [] # Create an empty list to store the obstacles
        self.running = True # A boolean variable to indicate if the game is running
        self.game_over = False # A boolean variable to indicate if the game is over
        self.hit_target = False # A boolean variable to indicate if the projectile has hit the target
        self.launched = False # A boolean variable to indicate if the projectile has been launched
        self.in_flight = False # A boolean variable to indicate if the projectile is in flight

        self.cannon = Cannon(self.cannon_x, self.cannon_y) # Create a cannon object with the specified position
        self.projectile = Projectile(self.projectile_x, self.projectile_y, self.projectile_vx, self.projectile_vy, self.projectile_m, self.projectile_Cd, self.B2, 9.81) # Create a projectile object with the specified position, velocity, mass, drag coefficient, and acceleration due to gravity
        self.target = Goal(self.target_x, self.target_y, self.target_width, self.target_height) # Create a target object with the specified position and size


    def obstacleManager(self): # A function to manage the obstacles
        self.obstacleList.clear() # Clear the list of obstacles
        for i in range(self.levelCounter): # Loop through the number of obstacles for the current level
            self.obstacleList.append(Obstacle(random.randint(0,self.SCREEN_WIDTH), random.randint(0,self.SCREEN_HEIGHT), random.randint(20,100), random.randint(20,100))) # Add an obstacle to the list of obstacles


    def run(self): # A method to run the game loop
        while self.running: # A loop to run the game while th boolean variable is True
            while not self.game_over: # A loop to run the game while the boolean variable is False
                """
                This section of the code is executed once per frame and will handle any events that occur
                """

                """UPDATE THE GAME STATE"""
                mouse_x, mouse_y = pygame.mouse.get_pos() # Get the position of the mouse in pixels inside the window
                angle = math.atan2(mouse_y - self.cannon_y, mouse_x - self.cannon_x) # Calculate the angle between the cannon and the mouse

                # Rotate the cannon based on the angle between the cannon and the mouse
                self.cannon = self.cannon.rot_center(math.degrees(angle))


                if self.launched: # If the projectile has been launched
                    self.power = ((mouse_x - self.cannon_x)**2 + (mouse_y - self.cannon_y)**2)**0.5 / 5 # Calculate the power of the projectile based on the distance between the cannon and the mouse
                    self.projectile.set_vx_vy(math.cos(-angle)*self.power, math.sin(-angle)*self.power) # Set the x-velocity and y-velocity of the projectile based on the power and angle between the cannon and the mouse
                    self.launched = False # Set the boolean variable to False to indicate that the projectile has been launched
                    self.in_flight = True # Set the boolean variable to True to indicate that the projectile is in flight

                if self.in_flight: # If the projectile is in flight
                    self.projectile.update_position() # Call the method to update the position of the projectile
                    if self.projectile.y > self.SCREEN_HEIGHT: # If the projectile has gone out of the screen
                        self.in_flight = False # Set the boolean variable to False to indicate that the projectile is no longer in flight

                if self.target.check_collision(self.projectile): # Call the method to check if the projectile has hit the target
                    self.hit_target = True # Set the boolean variable to True to indicate that the projectile has hit the target
                    self.levelCounter += 1 # Increase the level counter by 1
                    self.newTargetPosition() # Call the function to set the position of the target
                    self.obstacleManager() # Call the function to manage the obstacles
                    break

                for i in range(len(self.obstacleList)): # Run through the list of obstacles
                    if self.obstacleList[i].check_collision(self.projectile) and not self.in_flight: # If the projectile has hit an obstacle and is not in flight
                        self.obstacleManager() # Call the function to manage the obstacles
                    elif self.obstacleList[i].check_collision(self.projectile) and self.in_flight: # If the projectile has hit an obstacle and is in flight
                        self.projectile.bounce(1) # Call the method to bounce the projectile off the obstacle
                        break # Break out of the loop

                if self.projectile.x < 0 or self.projectile.x > self.SCREEN_WIDTH or self.projectile.y > self.SCREEN_HEIGHT: # If the projectile has gone out of the screen 
                    break # Break out of the loop

                """EVENT HANDLING"""
                for event in pygame.event.get(): # Get all the events that occur
                    if event.type == pygame.QUIT: # If the user clicks the close button, end the game
                        self.running = False # Set the boolean variable to False to indicate that the game is over
                        self.game_over = True # Set the boolean variable to True to indicate that the game is over
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN: # If the user clicks the mouse
                        if event.button == 1: # If the user clicks the left mouse button
                            if not self.launched and not self.in_flight: # If the projectile has not been launched and is not in flight
                                self.launched = True # Set the boolean variable to True to indicate that the projectile has been launched
                                self.projectile_colour = (random.randint(70, 255), random.randint(70, 255), random.randint(70, 255)) # Set the colour of the projectile tracer to a random colour
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
                            if not self.launched and not self.in_flight: # If the projectile has not been launched and is not in flight
                                self.launched = True # Set the boolean variable to True to indicate that the projectile has been launched
                                self.projectile_colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) # Set the colour of the projectile tracer to a random colour
                            else: # If the projectile has been launched or is in flight
                                pass # Do nothing

                """DRAW THE GAME STATE"""
                self.screen.fill(self.bg_color) # Fill the screen with the background color
                # Draw the cannon image on the screen
                self.screen.blit(self.cannon_image, (self.cannon_x - self.cannon_image.get_width() // 2, self.cannon_y - self.cannon_image.get_height() // 2))
                self.target.draw(self.screen) # Draw the target on the screen

                for i in range(len(self.obstacleList)): # Loop through the list of obstacles
                    self.obstacleList[i].draw(self.screen) # Draw the obstacle on the screen

                pygame.draw.circle(self.screen, (self.projectile_colour), (int(self.projectile.x), int(self.projectile.y)), 5) # Draw the projectile on the screen
                if len(self.projectile.trajectory) > 1: # If the projectile has a trajectory
                    pygame.draw.lines(self.screen, self.projectile_colour, False, self.projectile.trajectory, 2) # Draw the trajectory of the projectile on the screen

                font = pygame.font.SysFont("consolas", 20) # Set the font and size of the text that will be displayed on the screen
                text = font.render(f"Cannon Velocity: {round(self.projectile.vx, 2)}, {round(self.projectile.vy, 2)}", True, (255, 255, 255)) # Write the x-velocity and y-velocity of the cannon on the screen and round the values to 2 decimal places. Text is white
                self.screen.blit(text, (10, 10)) # Draw the text on the screen
                text = font.render(f"Drag Coefficient: " + str(self.projectile_Cd) + ", Mass: " + str(self.projectile_m) + "Kg, Air Resistance: " + str(self.B2), True, (255, 255, 255)) # Write the drag coefficient, mass, and air resistance of the projectile on the screen. Text is white
                self.screen.blit(text, (10, 30)) # Draw the text on the screen
                pygame.display.flip() # Update the screen
                
        pygame.quit() # Quit the game

game = Game() # Create an instance of the Game class
game.run()