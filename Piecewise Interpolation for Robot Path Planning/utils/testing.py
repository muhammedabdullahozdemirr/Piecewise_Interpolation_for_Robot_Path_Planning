import numpy as np

# Import interpolation methods - add this import
from interpolation import (
    newton_interpolate,
    lagrange_interpolate, 
    cubic_spline_interpolate,
    b_spline_interpolate
)

def analytical_function(x, test_type='linear'):
    """Analytical function for testing interpolation accuracy"""
    if test_type == 'linear':
        return x
    elif test_type == 'quadratic':
        return x**2
    elif test_type == 'cubic':
        return x**3
    elif test_type == 'sine':
        return np.sin(x)
    elif test_type == 'runge':
        return 1/(1 + 25*x**2)
    else:
        return x

def test_method_on_function(method_func, test_type, num_sample_points=5, num_test_points=100):
    """Test interpolation method on analytical function"""
    # Generate sample points
    if test_type == 'runge':
        x_range = [-1, 1]
    else:
        x_range = [0, 1]
        
    x_sample = np.linspace(x_range[0], x_range[1], num_sample_points)
    y_sample = analytical_function(x_sample, test_type)
    waypoints = np.column_stack((x_sample, y_sample))
    
    # Generate ground truth for comparison
    x_test = np.linspace(x_range[0], x_range[1], num_test_points)
    y_true = analytical_function(x_test, test_type)
    
    # Run interpolation
    try:
        path = method_func(waypoints)
        
        # Extract y values at test points (assuming uniform x spacing in result)
        y_interp = np.interp(x_test, path[:, 0], path[:, 1])
        
        # Calculate error
        error = np.abs(y_interp - y_true)
        max_error = np.max(error)
        mean_error = np.mean(error)
        
        # Determine if test passed
        tolerance = 0.1
        if test_type == 'linear':
            tolerance = 0.01
        elif test_type == 'quadratic' and method_func.__name__ == 'cubic_spline_interpolate':
            tolerance = 0.02
        elif test_type == 'quadratic' and method_func.__name__ == 'b_spline_interpolate':
            tolerance = 0.05
        
        passed = max_error < tolerance
        
        return {
            'passed': passed,
            'max_error': max_error,
            'mean_error': mean_error,
            'error_message': f"Max error: {max_error:.6f}, Mean error: {mean_error:.6f}"
        }
        
    except Exception as e:
        return {
            'passed': False,
            'error_message': f"Exception: {str(e)}"
        }

def run_method_tests(method_name):
    """Run all tests for a given interpolation method"""
    if method_name == 'newton':
        method_func = newton_interpolate
    elif method_name == 'lagrange':
        method_func = lagrange_interpolate
    elif method_name == 'cubic_spline':
        method_func = cubic_spline_interpolate
    elif method_name == 'b_spline':
        method_func = b_spline_interpolate
    else:
        return False, {"unknown_method": {"passed": False, "error_message": "Unknown method"}}
    
    # Define test cases
    test_cases = ['linear', 'quadratic']
    
    # Add specific test cases for each method
    if method_name == 'newton' or method_name == 'lagrange':
        test_cases.append('cubic')
    
    if method_name == 'cubic_spline' or method_name == 'b_spline':
        test_cases.append('sine')
    
    # Run tests
    results = {}
    all_passed = True
    
    for test_case in test_cases:
        result = test_method_on_function(method_func, test_case)
        results[test_case] = result
        if not result['passed']:
            all_passed = False
    
    return all_passed, results