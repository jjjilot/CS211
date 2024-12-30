import matplotlib.pyplot as plt
from numpy import pi, arange
from math import sin

x = [i for i in arange(0, 2 * pi, 2*pi/100)]
y = [sin(i) for i in x]

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()