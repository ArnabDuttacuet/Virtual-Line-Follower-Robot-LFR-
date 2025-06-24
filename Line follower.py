"""Virtual Line-Follower"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Path definition
x= np.linspace(10, 90, 1000)
y= (50 + 
    20 * np.sin(np.pi * (x - 10) / 50)          # broad wave
    + 10 * np.sin(2 * np.pi * (x - 10) / 30))   # tighter wave
path = np.column_stack((x, y))                  # (N,2) array

# Figure setup
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect('equal')
ax.set_facecolor('white')
ax.plot(x, y, 'k', linewidth=8)                # drawing the  road

# Robot state 
robot_pos   = path[0].astype(float)                      # start point
robot_speed = 5.0                                        # px per frame
robot_rad   = 2.5
marker      = plt.Circle(robot_pos, robot_rad, color='royalblue')
ax.add_patch(marker)

# Animation setup 
next_idx = 1                                             # next waypoint
def update(_):
    global robot_pos, next_idx

    if next_idx >= len(path):
        return marker,                                   # finished

    target = path[next_idx]
    vec    = target - robot_pos
    dist   = np.linalg.norm(vec)

    # If we can reach or pass the waypoint this frame, snap to it
    if dist <= robot_speed:
        robot_pos[:] = target
        next_idx    += 1
    else:
        robot_pos[:] += (vec / dist) * robot_speed       # step toward it

    marker.center = robot_pos
    return marker,

# Run animation
ani = animation.FuncAnimation(fig,
                              update,
                              frames=len(path)+200,
                              interval=30,
                              blit=True)
plt.title("Virtual Line-Follower")
plt.show()




