import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# ---------- Parametric heart surface ----------
# This formula makes a smooth heart-like surface in 3D
def heart_surface(u, v):
    # u ∈ [0, pi], v ∈ [0, 2pi]
    x = 16 * (np.sin(u) ** 3) * np.sin(v)
    y = (13 * np.cos(u) - 5 * np.cos(2*u) - 2 * np.cos(3*u) - np.cos(4*u)) * np.sin(v)
    z = (13 * np.cos(u) - 5 * np.cos(2*u) - 2 * np.cos(3*u) - np.cos(4*u)) * np.cos(v)
    return x, y, z

# Create meshgrid for parameters
u = np.linspace(0, np.pi, 60)
v = np.linspace(0, 2*np.pi, 60)
U, V = np.meshgrid(u, v)
X, Y, Z = heart_surface(U, V)

# ---------- Plot ----------
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection="3d")

surf = [ax.plot_surface(X, Y, Z, color="red", alpha=1.0, linewidth=0, antialiased=True)]

ax.set_box_aspect((1,1,1))
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])

# ---------- Rotation animation ----------
def update(angle):
    ax.view_init(elev=20, azim=angle)
    return surf

ani = FuncAnimation(fig, update, frames=np.linspace(0, 360, 120), interval=50, blit=False)

plt.show()
