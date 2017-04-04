import time                                                     # for sleep and keeping track of runtimes
import numpy as np                                              # numpy!    
# from scipy import integrate                                   # formerly used when I was testing / animating the lorenz attractor

from matplotlib import pyplot as plt                            # see next comment
from mpl_toolkits.mplot3d import Axes3D                         #
from matplotlib.colors import cnames                            #
from matplotlib import animation                                # fairly self-explanatory
import modded_backend as backend                                # import your own simulation function HERE!


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
    steps = 2000                                              # number of timesteps per frame                                                         
    i = (steps * i) % x_t.shape[1]                            # to be honest I have no idea what this does but it makes my animations work.  Seriously, what is it?
    for line, pt, xi in zip(lines, pts, x_t):                 # iterates through all trajectories by matching them to a line and point at some time step
        x, y, z = xi[:i].T                                    # also don't know what this does
        # print("xi is", xi)                                  # holdovers from when I couldn't figure out wtf was going on 
        # print("xi shit is", xi[:i])                         # holdovers from when I couldn't figure out wtf was going on 
        # print(type(xi[:i]))                                 # holdovers from when I couldn't figure out wtf was going on 
        # print("showing the transpose shit", xi[:i].T)       # holdovers from when I couldn't figure out wtf was going on 
        # print('x,y,z are', x,y,z)                           # holdovers from when I couldn't figure out wtf was going on 
        # time.sleep(3)                                       # holdovers from when I couldn't figure out wtf was going on    
        line.set_data(x, y)                                   # adds the current data to the line or something?   
        line.set_3d_properties(z)                             # same but it's 3d so need z
        pt.set_data(x[-1:], y[-1:])                           # ...uh
        pt.set_3d_properties(z[-1:])                          # "it is obvious what this does so I won't document it"
    ax.view_init(90, 0.0001 * i)                              # this initializes the offset view of the axes, and sets a smooth rate of rotation (.0001*i) dependent on how far through
    fig.canvas.draw()                                         #  draw stuff idk man i'm no artist
    return lines + pts 

def wrapper(r_exp_tuple_list, position, velocity, k, m, step_size, numsteps):
    print("called wrapper")                                   # not Dr. Dre, sadly.  I wish I had him on dial.  
    first_time = time.time()                                  # because I have lots of other "start_time" defninitons sprinkled throughout
    for n_tuple in r_exp_tuple_list:                                      # iterate through a list of exponent values for r in newton's law of gravitation
        print("current job: r**(-", n_tuple,")")                    # when runtimes get long it's nice to know how far through you are
        # np.random.seed(1)
        # x0 = -2 + 4 * np.random.random((N_trajectories, 3))   # randomizes starting position for each trajectory
        # v0 = -1 + 2 * np.random.random((N_trajectories, 3))   # randomizes starting velocity for each trajectory
        # p0 = zip(x0,v0)                                       # iterates through and returns x0 and v0 pairs in one tuple, p0.  For ease in the list comprehension below. 
        # arguments for simulate: simulate(position, velocity, k, m, n, step_size, num_steps):
        global x_t                                            # so that the animate function can still use this
        x_t = np.asarray([backend.simulate(position,velocity,k,m,n_tuple,step_size,numsteps)]) # if you're outputting from your own function, make sure that it's an array of position vectors (also arrays!)
        # Set up figure & 3D axis for animation
        global fig                                            # 
        fig = plt.figure()                                    # 
        global ax                                             # 
        ax = fig.add_axes([0, 0, 1, 1], projection='3d')      # 
        ax.axis('off')                                        # sets the background axes "on".  Change to "off" if you want a more artistic/minimalistic viewing experience

        # choose a different color for each trajectory
        global colors
        colors = plt.cm.jet(np.linspace(0, 1, 1))

        # set up lines and points
        global lines
        lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
        global pts
        pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])

        # prepare the axes limits
        ax.set_xlim((-3, 3))
        ax.set_ylim((-3, 3))
        ax.set_zlim((-3, 3))

        # set point-of-view: specified by (altitude degrees, azimuth degrees)
        ax.view_init(90, 0)
        # instantiate the animator.
        start_time = time.time()
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=2000, interval=1, blit=True)
        print("anim_time is", time.time()-start_time)
        start_time = time.time()
        plt.show()
        # mywriter = animation.FFMpegWriter(bitrate=4000)   # you have to install FFMpeg if you want to write out to mp4
        # anim.save('single_orbit_n='+str(n)+'position_'+str(position)+'velocity'+str(velocity)+'.mp4', writer='ffmpeg', fps=60, extra_args=['-vcodec', 'libx264']) # autogenerate filenames and export
        # print("saved the file!")
        # print("savetime is", time.time()-start_time)
        # input()
        # plt.close()
    print('combined runtime is', time.time() - first_time)

wrapper([(2,1.5)],(.5,0,0),(0,1,0),1,1,.00001,200000)

