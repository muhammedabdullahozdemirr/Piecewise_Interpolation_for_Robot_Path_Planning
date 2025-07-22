
import numpy as np

def calculate_curvature(x, y):
    """
    Calculate curvature of a path at each point using finite differences.
    
    Curvature formula:
        κ = |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)
    
    Args:
        x (numpy.ndarray): Array of x coordinates
        y (numpy.ndarray): Array of y coordinates
        
    Returns:
        numpy.ndarray: Curvature at each point
    """
    # Ensure inputs are numpy arrays
    x = np.asarray(x)
    y = np.asarray(y)
    
    # Calculate first derivatives
    dx = np.gradient(x)
    dy = np.gradient(y)
    
    # Calculate second derivatives
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    
    # Calculate curvature
    numerator = np.abs(dx * ddy - dy * ddx)
    denominator = (dx**2 + dy**2)**(3/2)
    
    # Handle divide by zero (straight line segments)
    curvature = np.zeros_like(x)
    mask = denominator > 1e-10
    curvature[mask] = numerator[mask] / denominator[mask]
    
    return curvature



