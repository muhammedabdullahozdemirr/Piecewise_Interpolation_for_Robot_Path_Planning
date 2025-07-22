


import numpy as np

# Test waypoint sets
TEST_WAYPOINTS = {
    'simple_straight': [(100, 100), (700, 100)],
    'simple_curve': [(100, 100), (400, 300), (700, 100)],
    'complex': [(100, 100), (200, 300), (400, 200), 
                (500, 400), (700, 300)],
    'zigzag': [(100, 100), (200, 300), (300, 100), (400, 300), 
               (500, 100), (600, 300), (700, 100)],
    'sharp_turns': [(100, 100), (150, 100), (150, 300), 
                     (400, 300), (400, 100), (650, 100), (650, 300)],
    'circle': [(400 + 200*np.cos(t), 300 + 200*np.sin(t)) 
               for t in np.linspace(0, 2*np.pi, 8, endpoint=False)],
    'oval_track': [(400 + 300*np.cos(t), 300 + 200*np.sin(t)) 
                  for t in np.linspace(0, 2*np.pi, 12, endpoint=False)],
    'sparse_curve': [(100, 300), (400, 500), (700, 300)],
    'dense_curve': [(100 + 60*i, 300 + 200*np.sin(i*np.pi/5)) for i in range(11)]
}