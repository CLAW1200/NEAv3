import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

# define a function that returns all possible cuboids that can be created
# from a given net
def find_cuboids(net):
    # list to hold the cuboids
    cuboids = []
    
    # iterate over all possible ways to fold the net
    for i in range(len(net)):
        for j in range(len(net[i])):
            # create a new cuboid by folding the net along the current
            # axis and adding it to the list of cuboids
            cuboid = fold(net, i, j)
            cuboids.append(cuboid)
            
    # return the list of cuboids
    return cuboids

# define a function that folds a net along a given axis
def fold(net, i, j):
    # create the cuboid by folding the net along the given axis
    cuboid = []
    for row in net:
        cuboid_row = []
        for col in row:
            cuboid_row.append(col)
        cuboid.append(cuboid_row)
        
    # return the cuboid
    return cuboid

# define a function that draws a cuboid in 3D using Matplotlib
def draw_cuboid(cuboid):
    # create the figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # draw the cuboid
    x, y, z = cuboid[0]
    ax.plot([x, x], [y, y], [z, z+1], c='k')
    ax.plot([x+1, x+1], [y, y], [z, z+1], c='k')
    ax.plot([x, x+1], [y, y], [z, z], c='k')
    ax.plot([x, x+1], [y, y], [z+1, z+1], c='k')
    ax.plot([x, x], [y+1, y+1], [z, z+1], c='k')
    ax.plot([x+1, x+1], [y+1, y+1], [z, z+1], c='k')
    ax.plot([x, x+1], [y+1, y+1], [z, z], c='k')
    ax.plot([x, x+1], [y+1, y+1], [z+1, z+1], c='k')
    ax.plot([x, x], [y, y+1], [z, z], c='k')
    ax.plot([x, x], [y, y+1], [z+1, z+1], c='k')
    ax.plot([x+1, x+1], [y, y+1], [z, z], c='k')
    ax.plot([x+1, x+1], [y, y+1], [z+1, z+1], c='k')
    
if __name__ == "__main__":
    # create a simple net
    net = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # find all possible cuboids that can be created from the net
    cuboids = find_cuboids(net)
    
    # draw the first cuboid
    draw_cuboid(cuboids[0])
    
    # show the plot
    plt.show()