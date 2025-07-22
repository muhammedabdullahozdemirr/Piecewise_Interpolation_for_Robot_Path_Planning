import numpy as np
from config import TEST_WAYPOINTS

def get_test_waypoints(name='simple_curve'):
    """Get predefined test waypoints."""
    if name not in TEST_WAYPOINTS:
        raise ValueError(f"Test waypoints '{name}' not found")
    
    return np.array(TEST_WAYPOINTS[name])

def generate_random_waypoints(num_points=5, x_range=(100, 700), y_range=(100, 500)):
    """Generate random waypoints within the specified range."""
    x = np.random.uniform(x_range[0], x_range[1], num_points)
    y = np.random.uniform(y_range[0], y_range[1], num_points)
    
    return np.column_stack((x, y))

def generate_waypoints_with_density(base_waypoints, density_factor):
    """Generate waypoints with modified density."""
    base_waypoints = np.array(base_waypoints)
    
    if density_factor == 1.0:
        return base_waypoints
    
    if density_factor > 1.0:
        # Increase density
        n_waypoints = len(base_waypoints)
        n_new_waypoints = int(n_waypoints * density_factor)
        
        t = np.zeros(n_waypoints)
        for i in range(1, n_waypoints):
            t[i] = t[i-1] + np.sqrt(np.sum((base_waypoints[i] - base_waypoints[i-1])**2))
        
        if t[-1] == 0:
            return base_waypoints
        
        t = t / t[-1]
        t_new = np.linspace(0, 1, n_new_waypoints)
        
        x = np.interp(t_new, t, base_waypoints[:, 0])
        y = np.interp(t_new, t, base_waypoints[:, 1])
        
        return np.column_stack((x, y))
    else:
        # Decrease density
        step = max(1, int(1 / density_factor))
        return base_waypoints[::step]