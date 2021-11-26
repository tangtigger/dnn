import numpy as np

lg = 0.5

p = np.exp(lg)/(1+ np.exp(lg))

np.log(1/10)
np.log(10/1)
np.log(0.5)
np.log(1)

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
# fig = plt.figure()
ax = plt.axes(projection='3d')
import random

x= np.random.random(10000)
# y= np.random.random(0, 2, size =50)
y = x/(1-x)
z = np.log(y)
ax.scatter3D(x, y, z, c=z,);

fig = plt.figure()
plt.scatter(x, z)
plt.grid()
plt.xlabel('x')
plt.ylabel('y')


def sig(z):
    res = 1/(1+np.exp(-z))
    return res
z = sig(20*x + 20*y - 30)

sig(-4.6)

ax.scatter3D(x, y, z, c=z,);



# Data for three-dimensional scattered points
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
plt.show()


a = 3.001
b = a**2

a = (6.5+7.5)**2/2
b = 6.5**2
c = 7.5**2
c+b-a