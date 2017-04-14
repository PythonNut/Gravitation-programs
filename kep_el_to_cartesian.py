import math
import numpy as np

# def kepEqApprox(M,e, steps=100000):
# 	E = M
# 	for 
def weird_ass_arctan(y,x):
	if x>0:
		return math.atan(y/x)
	elif y >= 0 and x<0:
		return math.pi+math.atan(y/x)
	elif y < 0 and x<0:
		return math.atan(y/x) - math.pi
	elif y>0 and x==0:
		return math.pi/2
	elif y<0 and x==0:
		return -math.pi/2
	else:
		return "error!  undefined. "


def converter(a,e,i,omega, OMEGA, mean_anomaly, planetname='not given', mu_sun = (1.32712440018*(10**20))):
	""" converts from keplerian orbital elemeents to cartesian coordinates.  Specifically, we go from a, the semimajor
		axis, e, the eccentricity of orbit, i, the inclination to elleptic, omega, the argument of periapsis, OMEGA, 
		the longitude of the ascending node, T, the orbital period, and mean_anomaly, the mean anomaly  to values of 
		x,y, and z in a rotated coordinate frame, and v_x, v_y, v_z in that frame.  

		based on https://downloads.rene-schwarz.com/download/M001-Keplerian_Orbit_Elements_to_Cartesian_State_Vectors.pdf
	"""
	
	# we now solve Kepler's Equation, M(t)=E(t)-esin(E) for the eccentric anomaly E(t) with a numerical method
	print(planetname)
	eccentric_anomaly = mean_anomaly
	y = (math.sqrt(1+e)*math.sin(eccentric_anomaly/2))
	x = (math.sqrt(1-e)*math.sin(eccentric_anomaly/2))	
	true_anomaly = 2*weird_ass_arctan(y,x)
	central_distance = a*(1-e*math.cos(eccentric_anomaly))

	# we now calculate the orbit position and velocity in the frame of the orbiting body.  
	opx = math.cos(true_anomaly)*central_distance
	opy = math.sin(true_anomaly)*central_distance	
	opz = 0

	mult_factor = math.sqrt(mu_sun*a/(central_distance))
	ovx = -1*math.sin(eccentric_anomaly)*mult_factor
	ovy = math.cos(eccentric_anomaly)*math.sqrt(1-e**2)
	ovz = 0

	# use rotation matrices to transform into the inertial frame of the Sun
	p = [[],[],[]]
	p[0] = opx*(math.cos(omega)*math.cos(OMEGA)-math.sin(omega)*math.cos(i)*math.sin(OMEGA)) - opy*(math.sin(omega)*math.cos(OMEGA)+math.cos(omega)*math.cos(i)*math.sin(OMEGA))
	p[1] = opx*(math.cos(omega)*math.sin(OMEGA)+math.sin(omega)*math.cos(i)*math.cos(OMEGA)) + opy*(math.cos(omega)*math.cos(i)*math.cos(OMEGA)-math.sin(omega)*math.sin(OMEGA))
	p[2] = opx*(math.sin(omega)*math.sin(i))+opy*(math.cos(omega)*math.sin(i))

	v = [[],[],[]]
	v[0] = ovx*(math.cos(omega)*math.cos(OMEGA)-math.sin(omega)*math.cos(i)*math.sin(OMEGA)) - ovy*(math.sin(omega)*math.cos(OMEGA)+math.cos(omega)*math.cos(i)*math.sin(OMEGA))
	v[1] = ovx*(math.cos(omega)*math.sin(OMEGA)+math.sin(omega)*math.cos(i)*math.cos(OMEGA)) + ovy*(math.cos(omega)*math.cos(i)*math.cos(OMEGA)-math.sin(omega)*math.sin(OMEGA))
	v[2] = ovx*(math.sin(omega)*math.sin(i))+ovy*(math.cos(omega)*math.sin(i))

	p = np.asarray(p)
	v = np.asarray(v)
	return np.asarray([p,v])