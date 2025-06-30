# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 20:57:16 2025

@author: JYOTIRMOY
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from galpy.orbit import Orbit
from galpy.potential import MWPotential2014
from astropy import units as u

# Step 1: Load M67 orbit
m67_orbit = Orbit.from_name("M67", ro=8.0, vo=220.0)

# Step 2: Time array
ts = np.linspace(0, 1, 1000) * u.Gyr

# Step 3: Integrate orbit
m67_orbit.integrate(ts, MWPotential2014)

# Step 4: Setup plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_xlabel("X [kpc]")
ax.set_ylabel("Y [kpc]")
ax.set_title("Galactic Orbit of M67")
line, = ax.plot([], [], lw=2, color='blue', label='Orbit Path')
point, = ax.plot([], [], 'ro', label='M67 Now')
ax.legend()

# Step 5: Define animation functions
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def update(frame):
    if frame < 2:
        x = m67_orbit.x(ts[frame])
        y = m67_orbit.y(ts[frame])
        line.set_data([], [])
        point.set_data([x], [y])
    else:
        x_data = m67_orbit.x(ts[:frame])
        y_data = m67_orbit.y(ts[:frame])
        line.set_data(x_data, y_data)
        point.set_data([x_data[-1]], [y_data[-1]])  # always pass sequences
    return line, point


# Step 6: Create animation
ani = FuncAnimation(fig, update, frames=len(ts), init_func=init, blit=True, interval=20)

# Step 7: Save animation
ani.save("m67_orbit.gif", writer=PillowWriter(fps=30))

# Optional: static plot to verify
plt.figure(figsize=(6, 6))
plt.plot(m67_orbit.x(ts), m67_orbit.y(ts), 'b')
plt.xlabel('X [kpc]')
plt.ylabel('Y [kpc]')
plt.title('Static Orbit of M67')
plt.grid(True)
plt.show()

