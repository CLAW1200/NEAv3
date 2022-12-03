import math
import matplotlib.pyplot as plt

class Projectile:
    """
    A class to simulate the flight of a projectile.
    """
    
    def __init__(self, x0, y0, vx0, vy0, mass, Cd, B2):
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
        
        # Set the time step
        self.dt = 0.1
        
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
        """
        Update the position and velocity of the projectile using the equations of motion.
        """
        # Calculate the air resistance force
        self.Fx = -0.5 * self.Cd * self.B2 * self.vx * math.sqrt(self.vx**2 + self.vy**2)
        self.Fy = -0.5 * self.Cd * self.B2 * self.vy * math.sqrt(self.vx**2 + self.vy**2) - 9.8
        
        # Calculate the acceleration of the projectile
        self.ax = self.Fx / self.m
        self.ay = self.Fy / self.m
        
        # Update the position and velocity of the projectile
        self.x = self.x + self.vx * self.dt
        self.y = self.y + self.vy * self.dt
        self.vx = self.vx + self.ax * self.dt
        self.vy = self.vy + self.ay * self.dt
        
        # Add the new position of the projectile to the list of positions
        self.xs.append(self.x)
        self.ys.append(self.y)
        
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
    
    def plot_trajectory(self):
        """
        Plot the trajectory of the projectile.
        """
        plt.plot(self.xs, self.ys)
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        plt.title('Projectile Motion')
        plt.show()

# Prompt the user for the initial position and velocity of the projectile
x0 = float(input("Enter the initial x position of the projectile: "))
y0 = float(input("Enter the initial y position of the projectile: "))
vx0 = float(input("Enter the initial x velocity of the projectile: "))
vy0 = float(input("Enter the initial y velocity of the projectile: "))

# Prompt the user for the mass and drag coefficient of the projectile
m = float(input("Enter the mass of the projectile: "))
Cd = float(input("Enter the drag coefficient of the projectile: "))

# Set the constant for air resistance
B2 = 0.00004

# Create a Projectile object
projectile = Projectile(x0, y0, vx0, vy0, m, Cd, B2)

# Print the initial position and velocity of the projectile
print("Initial position: (%f, %f)" % projectile.get_position())
print("Initial velocity: (%f, %f)" % projectile.get_velocity())

# Simulate the flight of the projectile
while projectile.y >= 0:
    projectile.update_position()

# Print the final position and velocity of the projectile
print("Final position: (%f, %f)" % projectile.get_position())
print("Final velocity: (%f, %f)" % projectile.get_velocity())

# Plot the path of the projectile
projectile.plot_trajectory()
