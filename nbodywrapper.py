import time                                                     # for sleep and keeping track of runtimes
import numpy as np                                              # numpy!    
# from scipy import integrate                                   # formerly used when I was testing / animating the lorenz attractor

from matplotlib import pyplot as plt                            # see next comment
from mpl_toolkits.mplot3d import Axes3D                         #
from matplotlib.colors import cnames                            #
from matplotlib import animation                                # fairly self-explanatory
import nbodybackend                                             # import your own simulation function HERE!
from kep_el_to_cartesian import *

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
    steps = 2000                                               # number of timesteps per frame                                                         
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
        ax.set_xlim((-3000000000000, 3000000000000))
        ax.set_ylim((-3000000000000, 3000000000000))
        ax.set_zlim((-3000000000000, 3000000000000))

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

# remember: call converter by converter(a,e,i,omega, OMEGA, mean_anomaly, planetname='not given', mu_sun = (1.32712440018*(10**20)))

AU = 149597870700
cyr = 63141*AU
sun_mass = 1.989*(10**30)
sun_data = [sun_mass, [0,0,0], [0,0,0]]

# the following data are circa 


# -----------------------------------------------
mercury_mass = 3.285*(10**23)
mercury_aphelion = .466697*AU
mercury_perihelion = .301499*AU

mercury_semimajor_axis = 0.38709927*AU
mercury_eccentricity = 0.20563593
mercury_inclination = 7.00497902
mercury_mean_anomaly =  252.25032350
mercury_argument_of_periapsis =77.45779628
mercury_longitude_of_ascending_node = 48.33076593

cartesian_mercury = converter(mercury_semimajor_axis, mercury_eccentricity, mercury_inclination, mercury_argument_of_periapsis, mercury_longitude_of_ascending_node, mercury_mean_anomaly, "Mercury")
mercury_data = [mercury_mass, cartesian_mercury[0], cartesian_mercury[1]]
# -----------------------------------------------
venus_mass = 4.867*(10**24)
venus_aphelion = .728213*AU
venus_perihelion = .718440*AU

venus_semimajor_axis = 0.72333566*AU
venus_eccentricity = 0.00677672
venus_inclination = 3.39467605
venus_mean_anomaly = 181.97909950
venus_argument_of_periapsis =131.60246718
venus_longitude_of_ascending_node =76.67984255

cartesian_venus = converter(venus_semimajor_axis, venus_eccentricity, venus_inclination, venus_argument_of_periapsis, venus_longitude_of_ascending_node, venus_mean_anomaly, "Venus")
venus_data = [venus_mass, cartesian_venus[0], cartesian_venus[1]]
# -----------------------------------------------
earth_mass = 5.972*(10**24)
earth_aphelion = 1.017*AU
earth_perihelion = 0.98327*AU

earth_semimajor_axis = 1.00000261*AU
earth_eccentricity = 0.01671123
earth_inclination = -0.00001531
earth_mean_anomaly = 100.46457166
earth_argument_of_periapsis = 102.93768193
earth_longitude_of_ascending_node = 0.0

cartesian_earth = converter(earth_semimajor_axis, earth_eccentricity, earth_inclination, earth_argument_of_periapsis,  earth_longitude_of_ascending_node, earth_mean_anomaly, "Earth")
earth_data = [earth_mass, cartesian_earth[0], cartesian_earth[1]]
# -----------------------------------------------
mars_mass = 6.39*(10**23)
mars_aphelion = 1.6660*AU
mars_perihelion = 1.3814

mars_semimajor_axis =1.52371034*AU
mars_eccentricity = 0.09339410
mars_inclination = 1.84969142
mars_mean_anomaly = -4.55343205
mars_argument_of_periapsis =-23.94362959
mars_longitude_of_ascending_node =49.55953891

cartesian_mars = converter(mars_semimajor_axis, mars_eccentricity, mars_inclination, mars_argument_of_periapsis, mars_longitude_of_ascending_node, mars_mean_anomaly, "Mars")
mars_data = [mars_mass, cartesian_mars[0], cartesian_mars[1]]
# -----------------------------------------------
jupiter_mass = 1.898*(10**27)
jupiter_aphelion = 5.45492*AU
jupiter_perihelion =4.95029*AU

jupiter_semimajor_axis = 5.20288700*AU
jupiter_eccentricity = 0.04838624
jupiter_inclination = 1.30439695 
jupiter_mean_anomaly = 34.39644051
jupiter_argument_of_periapsis =  14.72847983
jupiter_longitude_of_ascending_node =100.47390909

cartesian_jupiter = converter(jupiter_semimajor_axis, jupiter_eccentricity, jupiter_inclination, jupiter_argument_of_periapsis, jupiter_longitude_of_ascending_node, jupiter_mean_anomaly, "Jupiter")
jupiter_data = [jupiter_mass, cartesian_jupiter[0], cartesian_jupiter[1]]
# -----------------------------------------------
saturn_mass = 5.683*(10**26)
saturn_aphelion = 10.086*AU
saturn_perihelion = 9.024*AU 

saturn_semimajor_axis = 9.53667594*AU
saturn_eccentricity = 0.05386179
saturn_inclination = 2.48599187
saturn_mean_anomaly = 49.95424423
saturn_argument_of_periapsis = 92.59887831
saturn_longitude_of_ascending_node = 113.66242448

cartesian_saturn = converter(saturn_semimajor_axis, saturn_eccentricity, saturn_inclination, saturn_argument_of_periapsis, saturn_longitude_of_ascending_node, saturn_mean_anomaly, "Saturn")
saturn_data = [saturn_mass, cartesian_saturn[0], cartesian_saturn[1]]
# -----------------------------------------------
uranus_mass = 8.681*(10**25)
uranus_aphelion = 20.11*AU
uranus_perihelion = 18.33*AU

uranus_semimajor_axis = 19.18916464*AU
uranus_eccentricity = 0.04725744
uranus_inclination = 0.77263783 
uranus_mean_anomaly = 313.23810451
uranus_argument_of_periapsis = 170.95427630
uranus_longitude_of_ascending_node = 74.01692503

cartesian_uranus = converter(uranus_semimajor_axis, uranus_eccentricity, uranus_inclination, uranus_argument_of_periapsis, uranus_longitude_of_ascending_node, uranus_mean_anomaly, "Uranus")
uranus_data = [uranus_mass, cartesian_uranus[0], cartesian_uranus[1]]
# -----------------------------------------------
neptune_mass = 1.024*(10**26)
neptune_aphelion = 30.33*AU
neptune_perihelion = 29.81*AU

neptune_semimajor_axis = 30.06992276*AU
neptune_eccentricity = 0.00859048
neptune_inclination = 1.77004347
neptune_mean_anomaly = -55.12002969
neptune_argument_of_periapsis = 44.96476227
neptune_longitude_of_ascending_node =131.78422574

cartesian_neptune = converter(neptune_semimajor_axis, neptune_eccentricity, neptune_inclination, neptune_argument_of_periapsis, neptune_longitude_of_ascending_node, neptune_mean_anomaly, "Neptune")
neptune_data = [neptune_mass, cartesian_neptune[0], cartesian_neptune[1]]

m_list = [sun_data, mercury_data, venus_data, earth_data, mars_data, jupiter_data, saturn_data, neptune_data, uranus_data]

step_size = .000000001
num_steps = 1000000
wrapper(G, m_list, step_size, num_steps, r_exp_list=[2])

