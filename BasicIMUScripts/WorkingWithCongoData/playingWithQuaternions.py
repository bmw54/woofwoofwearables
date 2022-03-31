import skinematics as skin
import numpy as np

rate = 100
t = np.arange(0,2,1/rate)
w = np.cos(t)
x = np.zeros_like(t)
y = np.zeros_like(t)
z = np.sin(t)

q = np.array([w,x,y,z]).transpose()

print(skin.quat.calc_angvel(q, rate))
print("\n\n")
print(skin.quat.quat2deg(q))

