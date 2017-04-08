import time                                                     # for sleep and keeping track of runtimes
import numpy as np                                              # numpy!    
# from scipy import integrate                                   # formerly used when I was testing / animating the lorenz attractor

from matplotlib import pyplot as plt                            # see next comment
from mpl_toolkits.mplot3d import Axes3D                         #
from matplotlib.colors import cnames                            #
from matplotlib import animation                                # fairly self-explanatory
import nbodybackend                                             # import your own simulation function HERE!

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
    steps = 20000                                               # number of timesteps per frame                                                         
    i = (steps * i) % x_t.shape[1]                            # to be honest I have no idea what this does but it makes my animations work.  Seriously, what is it?
    # print(x_t.shape)
    # print(len(pts))
    # print(len(lines))
    for line, pt, xi in zip(lines, pts, x_t):                 # iterates through all trajectories by matching them to a line and point at some time step
        # print('hello')
        # print('in loops')
        # print(i)
        # time.sleep(1)
        x, y, z = xi[:i].T                                    # also don't know what this does
        # print(xi)
        line.set_data(x, y)                                   # adds the current data to the line or something?   
        line.set_3d_properties(z)                             # same but it's 3d so need z
        pt.set_data(x[-1:], y[-1:])                           # ...uh
        pt.set_3d_properties(z[-1:])                          # "it is obvious what this does so I won't document it"
    # ax.view_init(90, 0.0001 * i)                            # this initializes the offset view of the axes, and sets a smooth rate of rotation (.0001*i) dependent on how far through
    ax.view_init(30, .0001*i)
    fig.canvas.draw()                                         #  draw stuff idk man i'm no artist
    # print('hello')
    return lines + pts 

def wrapper(G, m_list, step_size, num_steps, r_exp_list=[2]): #add back r_exp_list?
    print("called wrapper")                                   # not Dr. Dre, sadly.  I wish I had him on dial.  
    first_time = time.time()                                  # because I have lots of other "start_time" defninitons sprinkled throughout
    for n in r_exp_list:                                      # iterate through a list of exponent values for r in newton's law of gravitation
        print("current job: r**(-", n,")")                    # when runtimes get long it's nice to know how far through you are
        global x_t                                            # so that the animate function can still use this
        # x_t = np.asarray([nbodybackend.simulate(G, m_list, n, step_size, num_steps)]) # if you're outputting from your own function, make sure that it's an array of position vectors (also arrays!)
        x_t = np.asarray(nbodybackend.simulate(G, m_list, n, step_size, num_steps))
        print(x_t)
        # Set up figure & 3D axis for animation
        global fig                                            # 
        fig = plt.figure()                                    # 
        global ax                                             # 
        ax = fig.add_axes([0, 0, 1, 1], projection='3d')      # 
        ax.axis('on')                                         # sets the background axes "on".  Change to "off" if you want a more artistic/minimalistic viewing experience

        # choose a different color for each trajectory
        global colors
        colors = plt.cm.jet(np.linspace(0, 1, len(m_list)))

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
        ax.view_init(30, 0)
        # instantiate the animator.
        start_time = time.time()
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=2000, interval=1, blit=True)
        print("anim_time is", time.time()-start_time)
        start_time = time.time()
        plt.show()
        # mywriter = animation.FFMpegWriter(bitrate=4000)                                                                                # you have to install FFMpeg if you want to write out to mp4
        # anim.save('single_orbit_n='+str(n)+'position_'+str(position)+'velocity'+str(velocity)+'timestep'+str(step_size)+'numsteps'+str(numsteps)+'.mp4', writer='ffmpeg', fps=60, extra_args=['-vcodec', 'libx264']) # autogenerate filenames and export
        # print("saved the file!")
        # print("savetime is", time.time()-start_time)
        # input()
        plt.close()
    print('combined runtime is', time.time() - first_time)

G = 6.67*(10**(-11))

# AU = 149597870700
# sun_mass = 1.989*(10**30)
# r_sun = 0

# earth_mass = 5.972*(10**24)
# earth_aphelion = 1.017*AU
# earth_perihelion = 0.98327*AU

# mercury_mass = 3.285*10(**23)
# mercury_aphelion = .466697*AU
# mercury_perihelion = .301499*AU

# venus_mass = 4.867*(10**24)
# venus_aphelion = .728213*AU
# venus_perihelion = .718440*AU


# mars_mass = 6.39*(10**23)
# mars_aphelion = 1.6660*AU
# mars_perihelion = 1.3814


# jupiter_mass = 1.898*(10**27)
# jupiter_aphelion = 5.45492*AU
# jupiter_perihelion =4.95029*AU

# saturn_mass = 5.683*(10**26)
# saturn_aphelion = 10.086*AU
# saturn_perihelion = 9.024*AU 

# uranus_mass = 8.681*(10**25)
# uranus_aphelion = 20.11*AU
# uranus_perihelion = 18.33*AU

# neptune_mass = 1.024*(10**26)
# neptune_aphelion = 30.33*AU
# neptune_perihelion = 29.81*AU


m_list =[ [5000000000,(0,-1,0),(0,0,0)], [3,(0,1,0), (0,.01,0)], [3,(.1,1,0), (0,-.1,0)] ]
step_size = 0.000001
num_steps = 1000000
wrapper(G, m_list, step_size, num_steps, r_exp_list=[2])

