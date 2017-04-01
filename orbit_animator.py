import time
import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
import backend
N_trajectories = 5

def lorentz_deriv(coord, t0, sigma=10., beta=8./3, rho=28.0):
    """Compute the time-derivative of a Lorentz system."""
    x = coord[0]
    y = coord[1]
    z = coord[2]
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -2 + 4 * np.random.random((N_trajectories, 3))
v0 = -1 + 2 * np.random.random((N_trajectories, 3))
p0 = zip(x0,v0)
# Note: t0 is required for the odeint function, though it's not used here.

# Solve for the trajectories
# t = np.linspace(0, 4, 1000)
# x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t)
#                   for x0i in x0])
# print(p0)
x_t = np.asarray([backend.simulate(pi[0],pi[1],1,1,2,.00001,3000000) for pi in p0])

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('on')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

# set up lines and points
lines = sum([ax.plot([], [], [], '-', c=c)
             for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])

# prepare the axes limits
ax.set_xlim((-15, 15))
ax.set_ylim((-15, 15))
ax.set_zlim((-5, 5))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    steps = 3000  
    i = (steps * i) % x_t.shape[1]

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        # print("xi is", xi)
        # print("xi shit is", xi[:i])
        # print(type(xi[:i]))
        # print("showing the transpose shit", xi[:i].T)
        # print('x,y,z are', x,y,z)
        # time.sleep(3)
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])

    ax.view_init(30, 0.0001 * i)
    fig.canvas.draw()
    return lines + pts

# instantiate the animator.
start_time = time.time()
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=1000, interval=30, blit=True)
print("anim_time is", time.time()-start_time)
start_time = time.time()
# Save as mp4. This requires mplayer or ffmpeg to be installed
#anim.save('lorentz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])
plt.show()
mywriter = animation.FFMpegWriter()
anim.save(str(N_trajectories)+'_trajectories.mp4', writer='ffmpeg', fps=60, extra_args=['-vcodec', 'libx264'], bitrate=4000)
print("saved the file!")
print("savetime is", time.time()-start_time)
