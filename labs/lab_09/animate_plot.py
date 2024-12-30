import numpy as np
from math import sin, cos
from numpy import pi, arange
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate_plot(t, v1, v2):
    x = [] # these variables will be used to build the animation
    y = []
    z = []

    # function that draws each frame of the animation
    def animate(i):
        ax.clear()
        ax.set_xlim([0,n])
        ax.set_ylim([-1,1])
        
        x.append(i)
        y.append(v1[i])
        z.append(v2[i])
        ax.plot(x,y,z)

    # create the figure and axes objects
    fig, ax = plt.subplots()
    # run the animation
    ani = FuncAnimation(fig, animate, frames=n, interval=30, repeat=False)

    plt.show()

n = 100
x = [i for i in arange(0, 2 * pi, 2*pi/100)]
y1 = [sin(i) for i in x]
y2 = [cos(i) for i in x]
