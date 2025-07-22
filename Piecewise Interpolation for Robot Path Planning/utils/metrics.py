

import numpy as np
from simulation.physics import calculate_curvature

def path_length(path):
    """
    Calculate the total length of a path.
    
    Args:
        path (numpy.ndarray): Array of path points as [x, y] coordinates
        
    Returns:
        float: Total path length
    """
    if len(path) < 2:
        return 0.0
    
    # Calculate distances between consecutive points
    diff = path[1:] - path[:-1]
    segment_lengths = np.sqrt(np.sum(diff**2, axis=1))
    
    return np.sum(segment_lengths)

def path_deviation(original_points, interpolated_path):
    """
    Calculate the deviation of an interpolated path from original waypoints.
    
    Args:
        original_points (numpy.ndarray): Original waypoints
        interpolated_path (numpy.ndarray): Interpolated path
        
    Returns:
        dict: Dictionary with deviation metrics:
            - max_deviation: Maximum distance from any waypoint to path
            - mean_deviation: Mean distance from waypoints to path
            - waypoint_deviations: Array of distances for each waypoint
    """
    # For each original point, find the closest point on the interpolated path
    deviations = []
    
    for point in original_points:
        # Calculate distances to all path points
        distances = np.sqrt(np.sum((interpolated_path - point)**2, axis=1))
        # Find minimum distance
        min_distance = np.min(distances)
        deviations.append(min_distance)
    
    deviations = np.array(deviations)
    
    return {
        'max_deviation': np.max(deviations),
        'mean_deviation': np.mean(deviations),
        'waypoint_deviations': deviations
    }

def curvature_metrics(path, max_curvature=None):
    """
    Calculate curvature metrics for a path.
    
    Args:
        path (numpy.ndarray): Array of path points as [x, y] coordinates
        max_curvature (float): Maximum allowable curvature
        
    Returns:
        dict: Dictionary with curvature metrics:
            - curvature: Array of curvature values
            - max_curvature: Maximum curvature value
            - mean_curvature: Mean curvature
            - violation_count: Number of points exceeding max_curvature
            - violation_percentage: Percentage of points exceeding max_curvature
    """
    if len(path) < 3:
        return {
            'curvature': np.array([]),
            'max_curvature': 0.0,
            'mean_curvature': 0.0,
            'violation_count': 0,
            'violation_percentage': 0.0
        }
    
    # Calculate curvature
    curvature_values = calculate_curvature(path[:, 0], path[:, 1])
    
    # Calculate violation metrics if max_curvature is provided
    violation_count = 0
    violation_percentage = 0.0
    
    if max_curvature is not None:
        violation_indices = np.where(curvature_values > max_curvature)[0]
        violation_count = len(violation_indices)
        violation_percentage = 100.0 * violation_count / len(curvature_values)
    
    return {
        'curvature': curvature_values,
        'max_curvature': np.max(curvature_values) if len(curvature_values) > 0 else 0.0,
        'mean_curvature': np.mean(curvature_values) if len(curvature_values) > 0 else 0.0,
        'violation_count': violation_count,
        'violation_percentage': violation_percentage
    }

def compare_methods(waypoints, paths_dict, max_curvature=None):
    """
    Compare different interpolation methods.
    
    Args:
        waypoints (numpy.ndarray): Original waypoints
        paths_dict (dict): Dictionary of {method_name: path_array}
        max_curvature (float): Maximum allowable curvature
        
    Returns:
        dict: Dictionary with comparison metrics for each method
    """
    results = {}
    
    for method, path in paths_dict.items():
        # Calculate path metrics
        deviation = path_deviation(waypoints, path)
        curvature = curvature_metrics(path, max_curvature)
        path_len = path_length(path)
        
        results[method] = {
            'path_length': path_len,
            'max_deviation': deviation['max_deviation'],
            'mean_deviation': deviation['mean_deviation'],
            'max_curvature': curvature['max_curvature'],
            'mean_curvature': curvature['mean_curvature'],
            'curvature_violations': curvature['violation_count'],
            'violation_percentage': curvature['violation_percentage']
        }
    
    return results

def print_comparison_table(comparison_results):
    """
    Print a formatted table of comparison results.
    
    Args:
        comparison_results (dict): Output from compare_methods
    """
    headers = ['Method', 'Path Length', 'Max Dev', 'Mean Dev', 
               'Max Curv', 'Mean Curv', 'Violations', 'Viol %']
    
    # Format headers
    header_str = ' | '.join(headers)
    print(header_str)
    print('-' * len(header_str))
    
    # Print each method's results
    for method, metrics in comparison_results.items():
        values = [
            method,
            f"{metrics['path_length']:.2f}",
            f"{metrics['max_deviation']:.2f}",
            f"{metrics['mean_deviation']:.2f}",
            f"{metrics['max_curvature']:.4f}",
            f"{metrics['mean_curvature']:.4f}",
            f"{metrics['curvature_violations']}",
            f"{metrics['violation_percentage']:.1f}%"
        ]
        print(' | '.join(values))