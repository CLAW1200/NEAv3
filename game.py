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
        self.max_vel = 100 # Maximum velocity of the projectile
        self.wind_speed = 0 # Wind speed in m/s
        self.wind_angle = 0 # Wind direction in degrees
        self.wind_x = 0 # Wind speed in m/s (x-component)
        self.wind_y = 0 # Wind speed in m/s (y-component)
        self.hit_target = False # A boolean variable to indicate if the projectile has hit the target
        self.distance_traveled = 0 # The distance traveled by the 
        self.distance_traveled_x = 0 # The distance traveled by the projectile in the x-direction
        self.distance_traveled_y = 0 # The distance traveled by the projectile in the y-direction


        # Initialize the list of points in the projectile's trajectory
        self.trajectory = [] # A list of points that follow the projectile path

        # Set the time step
        self.dt = 0.05 # Time step is how often the position of the projectile is updated in the simulation (not the same as the frame rate)

        # Initialize the air resistance force using the drag formula
        self.Fx = -0.5 * Cd * B2 * vx0 * math.sqrt(vx0**2 + vy0**2) # The x-component of the air resistance force
        self.Fy = -0.5 * Cd * B2 * vy0 * math.sqrt(vx0**2 + vy0**2) # The y-component of the air resistance force

        # Initialize the acceleration of the projectile
        self.ax = self.Fx / self.m # The x-component of the acceleration of the projectile
        self.ay = self.Fy / self.m # The y-component of the acceleration of the projectile

        # Initialize the lists of positions
        self.xs = [self.x] # A list of the x-positions of the projectile
        self.ys = [self.y] # A list of the y-positions of the projectile

    def set_wind(self, wind_speed, wind_angle):
        """
        A method to set the wind speed and direction.
        """
        self.wind_speed = wind_speed
        self.wind_angle = wind_angle
        self.wind_x = self.wind_speed * math.cos(math.radians(self.wind_angle))
        self.wind_y = self.wind_speed * math.sin(math.radians(self.wind_angle))
    
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

        #Add wind speed to the air resistance force
        self.Fx = self.Fx + self.wind_x
        self.Fy = self.Fy - self.wind_y

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
        # Update the distance traveled by the projectile
        self.distance_traveled = self.distance_traveled + math.sqrt((self.xs[-1] - self.xs[-2])**2 + (self.ys[-1] - self.ys[-2])**2) # Update the distance traveled by the projectile
        self.distance_traveled_x = self.distance_traveled_x + math.sqrt((self.xs[-1] - self.xs[-2])**2) # Update the distance traveled by the projectile in the x-direction
        self.distance_traveled_y = self.distance_traveled_y + math.sqrt((self.ys[-1] - self.ys[-2])**2) # Update the distance traveled by the projectile in the y-direction

    def set_vx_vy(self, vx, vy):
        """
        A method to set the velocity of the projectile while ensuring that the velocity does not exceed the maximum velocity.
        """
        if vx > self.max_vel:
            self.vx = self.max_vel
        elif vx < -self.max_vel:
            self.vx = -self.max_vel
        else:
            self.vx = vx
        if vy > self.max_vel:
            self.vy = self.max_vel
        elif vy < -self.max_vel:
            self.vy = -self.max_vel
        else:
            self.vy = vy

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
        self.colour = (155, 255, 155) # Set the colour of the goal to a light green (pre defined colour and not a parameter)

    def draw(self, screen):
        """
        A method to draw the goal on the screen.
        """
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height)) # Draw the goal on the screen as a rectangle with the colour, position, and size specified by the attributes of the goal object

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
        self.collision_range = 50
        super().__init__(x, y, width, height) # Call the constructor of the Goal class
        self.colour = (255, 100, 100) # Set the colour of the obstacle to a light red (pre defined colour and not a parameter)
        self.bounceAbsorption = 0.7 # Set the absorption multiplier of the obstacle
        self.friction = 0.05 # Set the friction multiplier of the obstacle
    def get_coordinates(self):

        """
        A method to return the coordinates of the obstacle.
        """
        return self.x, self.y, self.x + self.width, self.y + self.height # Return the coordinates of the obstacle as a tuple

    def check_collision(self, projectile, projectileImage):
        """
        A method to check if the projectile has collided with the obstacle using Separating Axis Theorem.
        """
        p_x, p_y = projectile.get_position()
        p_width, p_height = projectileImage.get_size()
        o_x1, o_y1, o_x2, o_y2 = self.get_coordinates()
        o_x = (o_x1 + o_x2) / 2
        o_y = (o_y1 + o_y2) / 2
        o_width = o_x2 - o_x1
        o_height = o_y2 - o_y1
        
        # Calculate the overlapping distance along the X and Y axes
        overlap_x = (p_width + o_width) / 2 - abs(p_x - o_x)
        overlap_y = (p_height + o_height) / 2 - abs(p_y - o_y)

        # If there is no overlap along either axis, then there is no collision
        if overlap_x <= 0 or overlap_y <= 0:
            return False

        # Determine which axis has the smallest overlap and resolve the collision along that axis
        if overlap_x < overlap_y:
            if p_x < o_x:
                p_x = o_x1 - p_width / 2
            else:
                p_x = o_x2 + p_width / 2
            vx, vy = projectile.get_velocity()
            vx = -vx * self.bounceAbsorption
            vy = vy * (1 - self.friction)
        else:
            if p_y < o_y:
                p_y = o_y1 - p_height / 2
            else:
                p_y = o_y2 + p_height / 2
            vx, vy = projectile.get_velocity()
            vy = -vy * self.bounceAbsorption
            vx = vx * (1 - self.friction)
       
        #play ball sound with random volume
        ballSound = pygame.mixer.Sound(f"assets\\ball{random.randint(1,6)}.mp3")
        vol = (projectile.get_velocity()[0]**2 + projectile.get_velocity()[1]**2)**0.5/100 - 0.05
        if vol < 0:
            vol = 0
        ballSound.set_volume((vol))
        game.BallChannelCounter += 1
        if game.BallChannelCounter > 40:
            game.BallChannelCounter = 5
        channel = pygame.mixer.Channel(game.BallChannelCounter)
        if vol != 0:
            game.bounceCounter += 1
            try:
                if channel.get_busy():
                    self.i += 1
                else:
                    channel.play(ballSound)
            except:
                pass
        # Update the position and velocity of the projectile after the collision
        projectile.set_vx_vy(vx, vy)
        projectile.set_position(p_x, p_y)
        return True


class Cannon:
    def __init__(self, x, y):
        """
        Initialize the cannon with its position and size.
        """
        self.x = x
        self.y = y
        self.cannon_image = pygame.image.load("assets\cannonTube.png") # Load the cannon image from the assets folder
        self.rot_cannon_image = pygame.image.load("assets\cannonTube.png") # Load the cannon image from the assets folder
        self.scale = 1.1
        self.cannon_image = pygame.transform.scale(self.cannon_image, (self.cannon_image.get_width() * self.scale, self.cannon_image.get_height() * self.scale))
        self.rot_cannon_image = pygame.transform.scale(self.rot_cannon_image, (self.rot_cannon_image.get_width() * self.scale, self.rot_cannon_image.get_height() * self.scale))
        self.power = 0 # Create a variable to store the power of the cannon
        
    def get_center(self):
        """
        A method to return the center of the cannon.
        """
        return self.x + self.cannon_image.get_width() / 2, self.y + self.cannon_image.get_height() / 2 # Return the center of the cannon as a tuple

    def set_power(self, power):
        """
        A method to set the power of the cannon.
        """
        self.power = power

    def get_power(self):
        """
        A method to get the power of the cannon.
        """
        return self.power

    def draw(self, screen):
        """
        A method to draw the cannon on the screen.
        """
        screen.blit(self.rot_cannon_image, (self.x, self.y))

    def rot_center(self, angle):
        """
        A method to rotate the cannon image to the angle.
        """
        self.rot_cannon_image = pygame.transform.rotate(self.cannon_image, angle)


class ProjectileImage:
    def __init__(self, x, y, size):
        """
        Initialize the projectile image with its position and size.
        """
        self.x = x
        self.y = y
        self.size = size
        self.width = size
        self.height = size
        self.projectile_colour = (255, 255, 255)

    def draw(self, screen, x, y):
        pygame.draw.circle(screen, (self.projectile_colour), (int(x), int(y)), self.size) # Draw the projectile on the screen

    def set_position(self, x, y):
        """
        A method to set the position of the projectile image.
        """
        self.x = x
        self.y = y
    
    def set_colour(self, colour):
        """
        A method to set the colour of the projectile image.
        """
        self.projectile_colour = colour

    def get_size(self):
        """
        A method to get the size of the projectile image.
        """
        return self.width, self.height

class WindArrow:
    def __init__(self, x, y):
        """
        Initialize the wind arrow with its position and size.
        """
        self.x = x
        self.y = y
        self.size = 5
        self.colour = (255, 255, 255) 
    
    def draw(self, screen):
        #draw a triangle
        pygame.draw.polygon(screen, self.colour, ((self.x, self.y), (self.x + 40, self.y + 10), (self.x + 40, self.y - 10)))

    def set_position(self, x, y):
        """
        A method to set the position of the wind arrow.
        """
        self.x = x
        self.y = y
        
    def draw_rotate(self, angle, screen):
        """
        A method to rotate the triangle by a given angle
        """
        angle = -angle - 180
        center_x = self.x + 20
        center_y = self.y
        points = [(self.x, self.y), (self.x + 40, self.y + 10), (self.x + 40, self.y - 10)]
        rotated_points = []
        for point in points:
            x = (point[0] - center_x) * math.cos(math.radians(angle)) - (point[1] - center_y) * math.sin(math.radians(angle)) + center_x
            y = (point[0] - center_x) * math.sin(math.radians(angle)) + (point[1] - center_y) * math.cos(math.radians(angle)) + center_y
            rotated_points.append((x, y))
        pygame.draw.polygon(screen, self.colour, rotated_points)


class Game: # A class to represent the game loop
    def __init__(self):
        """
        Set up the game window variables and initialize pygame
        """
        pygame.init() # Initialize pygame
        self.clock = pygame.time.Clock() # Set frame rate
        self.SCREEN_WIDTH = 1000 # Set the width of the screen
        self.SCREEN_HEIGHT = 600 # Set the height of the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT)) # Create a screen with the specified width and height
        self.BallChannelCounter = 5 # Set the channel counter to 0
        """
        Set up environment variables
        """
        self.bg_colour = (30, 30, 30) # Set the background colour of the screen (pre defined colour and not a parameter)
        self.B2 = 0.00004 # Set the drag coefficient of the projectile (pre defined value and not a parameter)
        """
        Set up target variables
        """
        self.target_x = self.SCREEN_WIDTH - 100 # Set the initial x-position of the target in pixels
        self.target_y = self.SCREEN_HEIGHT - 100 # Set the initial y-position of the target in pixels
        self.target_width = 20 # Set the width of the target in pixels
        self.target_height = 20 # Set the height of the target in pixels
        """
        Set up projectile variables
        """
        self.projectile_x = 0 # Set the initial x-position of the projectile to the x-position of the cannon
        self.projectile_y = 0 # Set the initial y-position of the projectile to the y-position of the cannon
        self.projectile_vx = 0 # Set the initial x-velocity of the projectile to the x-velocity of the cannon
        self.projectile_vy = 0 # Set the initial y-velocity of the projectile to the y-velocity of the cannon
        self.projectile_m = 2 # Set the mass of the projectile
        self.projectile_Cd = 0.52 # Set the drag coefficient of the projectile
        self.projectile_colour = (255, 255, 255) # Set the colour of the projectile to white
        self.bounceCounter = 0 # Set the bounce counter to 0
        """
        Set up level variables
        """
        self.levelCounter = 0 # Create a variable to store the current level
        self.obstacleList = [] # Create an empty list to store the obstacles
        self.running = True # A boolean variable to indicate if the game is running
        self.game_over = False # A boolean variable to indicate if the game is over
        self.launched = False # A boolean variable to indicate if the projectile has been launched
        self.in_flight = False # A boolean variable to indicate if the projectile is in flight
        self.background = pygame.image.load("assets\\background.png") # Load the background image
        """
        Create a cannon object
        """
        self.cannon = Cannon(100, self.SCREEN_HEIGHT/2) # Create a cannon object with the specified position
        self.target = Goal(self.target_x, self.target_y, self.target_width, self.target_height) # Create a target object with the specified position and size

    def obstacleManager(self):
        """
        A function to manage obstacles
        """
        self.obstacleList.clear() # Clear the list of obstacles

        self.obstacleList.append(Obstacle(0, self.SCREEN_HEIGHT-5, self.SCREEN_WIDTH, 50)) # Create a floor object with the specified position and size
        self.obstacleList.append(Obstacle(0, -45, self.SCREEN_WIDTH, 50)) # Create a ceiling object with the specified position and size
        self.obstacleList.append(Obstacle(self.SCREEN_WIDTH-5, 0, 50, self.SCREEN_HEIGHT)) # Create a right wall object with the specified position and size

        for i in range(self.levelCounter): # Loop through the number of obstacles for the current level
            self.obstacleList.append(Obstacle(random.randint(0,self.SCREEN_WIDTH), random.randint(0,self.SCREEN_HEIGHT), random.randint(20,100), random.randint(20,100))) # Add an obstacle to the list of obstacles

    def levelManager(self, state):
        if state == True:
            self.levelCounter += 2 # Increase the level counter 
            self.target = Goal(self.target_x, random.randint(50, self.SCREEN_HEIGHT-50), self.target_width, self.target_height) # Create a target object with the specified position and size
            self.obstacleManager() # Call the function to manage the obstacles
            self.projectile.set_wind((random.random() * self.levelCounter/4), random.randint(0,360))
            self.projectileImage.set_colour((random.randint(100,255), random.randint(100,255), random.randint(100,255))) # Set the colour of the projectile to a random colour
            self.game_over = True # Set the boolean variable to True to indicate that the game is over
        else:
            self.game_over = True # Set the boolean variable to True to indicate that the game is over


    def run(self):
        """
        A function to run the game loop
        """

        """Set Level Start Conditions"""
        self.projectile = Projectile(self.cannon.get_center()[0], self.cannon.get_center()[1], self.projectile_vx, self.projectile_vy, self.projectile_m, self.projectile_Cd, self.B2, 9.81) # Create a projectile object with the specified position, velocity, mass, drag coefficient, and acceleration due to gravity
        self.projectileImage = ProjectileImage(self.cannon.get_center()[0], self.cannon.get_center()[1], 5) # Create a projectile image object with the specified position and size
        self.windArrow = WindArrow(30, 70)
        self.obstacleManager()
        pygame.mixer.set_num_channels(41)

        #play amb1 sound on loop on channel 4
        sound = pygame.mixer.Sound("assets\\amb1.mp3")
        channel = pygame.mixer.Channel(4)
        channel.play(sound, -1)
        pygame.mixer.music.load("assets\\wind.mp3")
        pygame.mixer.music.play(-1)

        while self.running: # A loop to run the game while th boolean variable is True
            pygame.mixer.music.set_volume(self.projectile.wind_speed/10)
            self.projectile.set_position(self.cannon.get_center()[0], self.cannon.get_center()[1]) # Set the position of the projectile to the position of the cannon
            self.projectile.distance_traveled = 0 # Set the distance traveled to 0
            self.projectile.distance_traveled_x = 0 # Set the distance traveled in the x-direction to 0
            self.projectile.distance_traveled_y = 0 # Set the distance traveled in the y-direction to 0
            self.projectileImage.set_position(self.cannon.get_center()[0], self.cannon.get_center()[1]) # Set the position of the projectile image to the position of the cannon
            self.projectile.hit_target = False # A boolean variable to indicate if the projectile has hit the target
            self.game_over = False # A boolean variable to indicate if the game is over
            self.launched = False # A boolean variable to indicate if the projectile has been launched
            self.in_flight = False # A boolean variable to indicate if the projectile is in flight
            self.projectile.trajectory.clear() # Clear the trajectory list            
            self.bounceCounter = 0 # Set the bounce counter to 0

            while not self.game_over: # A loop to run the game while the boolean variable is False

                """
                This section of the code is executed once per frame and will handle any events that occur
                """

                """UPDATE THE GAME STATE"""
                mouse_x, mouse_y = pygame.mouse.get_pos() # Get the position of the mouse in pixels inside the window
                angle_projectile = (math.atan2(mouse_y - self.projectile.y, mouse_x -  self.projectile.x)) # Calculate the angle between the projectile and the mouse
                angle_cannon = (math.atan2(mouse_y - self.projectile.y, mouse_x -  self.projectile.x)) # Calculate the angle between the cannon and the mouse

                if not self.in_flight: # If the projectile is not in flight
                    self.cannon.rot_center(math.degrees(-angle_cannon)-20)
                    self.cannon.set_power(((mouse_x -  self.cannon.x)**2 + (mouse_y - self.cannon.y)**2)**0.5 / 5) # Calculate the power of the projectile based on the distance between the cannon and the mouse
                    self.projectile.set_vx_vy(math.cos(-angle_projectile)*self.cannon.get_power(), math.sin(-angle_projectile)*self.cannon.get_power()) # Set the x-velocity and y-velocity of the projectile based on the power and angle between the cannon and the mouse

                if self.launched: # If the projectile has been launched
                    self.cannon.set_power(((mouse_x -  self.cannon.x)**2 + (mouse_y - self.cannon.y)**2)**0.5 / 5) # Calculate the power of the projectile based on the distance between the cannon and the mouse
                    self.projectile.set_vx_vy(math.cos(-angle_projectile)*self.cannon.get_power(), math.sin(-angle_projectile)*self.cannon.get_power()) # Set the x-velocity and y-velocity of the projectile based on the power and angle between the cannon and the mouse
                    self.launched = False # Set the boolean variable to False to indicate that the projectile has been launched
                    self.in_flight = True # Set the boolean variable to True to indicate that the projectile is in flight

                if self.in_flight: # If the projectile is in flight
                    self.projectile.update_position() # Call the method to update the position of the projectile

                if self.target.check_collision(self.projectile): # Call the method to check if the projectile has hit the target
                    self.projectile.hit_target = True # Set the boolean variable to True to indicate that the projectile has hit the target
                    self.levelManager(self.projectile.hit_target) # Call the function to manage the levels
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets\\dingup.mp3'))
                for i in range(len(self.obstacleList)): # Run through the list of obstacles
                    #check collision with projectile or target
                    if self.obstacleList[i].check_collision(self.projectile, self.projectileImage) and not self.in_flight : # Call the method to check if the projectile or target has hit the obstacle
                        self.obstacleManager() # Call the function to manage the obstacles

                if self.projectile.x < 0 or self.projectile.x > self.SCREEN_WIDTH or self.projectile.y > self.SCREEN_HEIGHT or self.projectile.x < 0:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets\\error.mp3'))
                    break

                """EVENT HANDLING"""
                for event in pygame.event.get(): # Get all the events that occur
                    if event.type == pygame.QUIT: # If the user clicks the close button, end the game
                        self.running = False # Set the boolean variable to False to indicate that the game is over
                        self.game_over = True # Set the boolean variable to True to indicate that the game is over
                        break
                    if event.type == pygame.KEYDOWN: # If the user presses a key
                        if event.key == pygame.K_l:
                            self.game_over = True
                            self.levelManager(True)
                    elif event.type == pygame.MOUSEBUTTONDOWN: # If the user clicks the mouse
                        if event.button == 1: # If the user clicks the left mouse button
                            if not self.launched and not self.in_flight: # If the projectile has not been launched and is not in flight
                                self.launched = True # Set the boolean variable to True to indicate that the projectile has been launched
                            else: # If the projectile has been launched or is in flight
                                self.game_over = True # Set the boolean variable to True to indicate that the game is over 
                                
                """DRAW THE GAME STATE"""
                self.screen.fill(self.bg_colour) # Fill the screen with the background colour
                #draw background image
                self.screen.blit(self.background, (0,0))
                if self.in_flight:
                    self.projectileImage.draw(self.screen, self.projectile.x, self.projectile.y) # Draw the projectile on the screen
                self.cannon.draw(self.screen) # Draw the cannon on the screen
                self.target.draw(self.screen) # Draw the target on the screen
                for i in range(len(self.obstacleList)): # Loop through the list of obstacles
                    self.obstacleList[i].draw(self.screen) # Draw the obstacle on the screen

                self.windArrow.draw_rotate(self.projectile.wind_angle, self.screen) # Draw the wind arrow on the screen

                if len(self.projectile.trajectory) > 1: # If the projectile has a trajectory
                    pygame.draw.lines(self.screen, self.projectileImage.projectile_colour, False, self.projectile.trajectory[-1000:], 1) # Draw the trajectory of the projectile on the screen

                font = pygame.font.SysFont("consolas", 20) # Set the font and size of the text that will be displayed on the screen
                text = font.render(f"Cannon Velocity: {round(self.projectile.vx, 2)}, {round(self.projectile.vy, 2)} Wind Speed: {round(self.projectile.wind_speed,4)}m/s", True, (255, 255, 255)) # Write the x-velocity and y-velocity of the cannon on the screen and round the values to 2 decimal places. Text is white
                self.screen.blit(text, (10, 10)) # Draw the text on the screen
                text = font.render(f"Drag Coefficient: " + str(self.projectile_Cd) + ", Mass: " + str(self.projectile_m) + "Kg, Air Resistance: " + str(self.B2), True, (255, 255, 255)) # Write the drag coefficient, mass, and air resistance of the projectile on the screen. Text is white
                self.screen.blit(text, (10, 30)) # Draw the text on the screen
                text = font.render(f"Bounces: {self.bounceCounter}", True, (255, 255, 255)) # Write the wind angle on the screen and round the value to 4 decimal places. Text is white
                self.screen.blit(text, (10, 50)) # Draw the text on the screen

                pygame.display.flip() # Update the screen

        pygame.quit() # Quit the game

game = Game() # Create an instance of the Game class
game.run()