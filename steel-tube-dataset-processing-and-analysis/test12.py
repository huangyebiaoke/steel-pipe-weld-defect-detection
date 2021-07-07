import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import math



x=np.arange(100-10,2200+10,step=10)
# t=0.28
t=-2*math.pow(10,-3.3)
y=1.06*math.pow(10,12)*np.exp(x*t)+1
dot_x=[100,800,1500,2200]
dot_y=[1.06*math.pow(10,12),7.15*math.pow(10,11),5.98*math.pow(10,11),5.5*math.pow(10,11)]
plt.plot(x,y)
plt.scatter(dot_x,dot_y, s=8, c='r', alpha=0.4)
plt.title('test')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

