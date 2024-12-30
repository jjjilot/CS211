from random import random
from math import sin
import matplotlib.pyplot as plt

n_points = 100
x = [random() for i in range(n_points)]
y = [random() for i in range(n_points)]

fig, ax = plt.subplots()
ax.scatter(x, y)
plt.show()