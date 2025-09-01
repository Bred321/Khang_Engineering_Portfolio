import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -------- Heart equation (implicit surface) --------
def heart_function(x, y, z):
    return (x**2 + (9/4)*y**2 + z**2 - 1)**3 - x**2*z**3 - (9/80)*y**2*z**3

# -------- Grid --------
grid = 100
bound = 1.5
x = np.linspace(-bound, bound, grid)
y = np.linspace(-bound, bound, grid)
X, Y = np.meshgrid(x, y)

# -------- Compute Z from implicit equation --------
Z_upper = np.zeros_like(X)
Z_lower = np.zeros_like(X)

for i in range(grid):
    for j in range(grid):
        # Solve heart_function(x,y,z)=0 for z
        xi, yi = X[i, j], Y[i, j]
        z_vals = np.linspace(-1.5, 1.5, 200)
        f_vals = heart_function(xi, yi, z_vals)
        idx = np.where(np.sign(f_vals[:-1]) != np.sign(f_vals[1:]))[0]
        if len(idx) >= 1:
            Z_lower[i, j] = z_vals[idx[0]]
            Z_upper[i, j] = z_vals[idx[-1]]
        else:
            Z_lower[i, j] = np.nan
            Z_upper[i, j] = np.nan

# -------- Plot --------
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(X, Y, Z_upper, color="red", alpha=1.0, rstride=1, cstride=1, linewidth=0)
ax.plot_surface(X, Y, Z_lower, color="red", alpha=1.0, rstride=1, cstride=1, linewidth=0)

ax.set_box_aspect((1,1,1))
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
ax.set_title("3D Red Heart")

plt.show()
