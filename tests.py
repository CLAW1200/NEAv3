import math
def pol(vel, angle):
    return vel * math.cos(angle), -1 * vel * math.sin(angle)

print(pol(0, 0))