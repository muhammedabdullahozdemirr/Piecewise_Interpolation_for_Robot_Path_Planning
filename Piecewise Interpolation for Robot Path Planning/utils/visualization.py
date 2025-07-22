import numpy as np
import matplotlib.pyplot as plt

def plot_interpolation_comparison(waypoints, paths):
    """Create comparison plot for different interpolation methods."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot waypoints
    ax.plot(waypoints[:, 0], waypoints[:, 1], 'ro-', markersize=8, label='Waypoints')
    
    # Plot each path
    colors = ['blue', 'green', 'purple', 'orange']
    for i, (method, path) in enumerate(paths.items()):
        color = colors[i % len(colors)]
        ax.plot(path[:, 0], path[:, 1], color=color, linewidth=2, label=method)
    
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Path Comparison')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return fig

def plot_curvature_comparison(paths, curvatures):
    """Plot curvature profiles for different methods."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['blue', 'green', 'purple', 'orange']
    for i, (method, curvature) in enumerate(curvatures.items()):
        color = colors[i % len(colors)]
        path = paths[method]
        
        # Create parameter along path (arc length)
        t = np.zeros(len(path))
        for j in range(1, len(path)):
            t[j] = t[j-1] + np.sqrt(np.sum((path[j] - path[j-1])**2))
        
        # Normalize t to [0, 1]
        if t[-1] > 0:
            t = t / t[-1]
        
        ax.plot(t, curvature, color=color, label=method)
    
    ax.set_xlabel('Normalized Path Length')
    ax.set_ylabel('Curvature')
    ax.set_title('Curvature Comparison')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return fig

def plot_local_control_effect(methods, original_waypoints, modified_waypoints, 
                            original_paths, modified_paths):
    """Visualize how changing one waypoint affects the entire curve."""
    num_methods = len(methods)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, method in enumerate(methods):
        ax = axes[i]
        
        # Plot original data
        ax.plot(original_waypoints[:, 0], original_waypoints[:, 1], 'ro-', alpha=0.5, label='Original waypoints')
        ax.plot(original_paths[method][:, 0], original_paths[method][:, 1], 'b-', alpha=0.5, label='Original path')
        
        # Plot modified data
        ax.plot(modified_waypoints[:, 0], modified_waypoints[:, 1], 'mo-', label='Modified waypoints')
        ax.plot(modified_paths[method][:, 0], modified_paths[method][:, 1], 'g-', label='Modified path')
        
        # Find point that was modified
        mid_idx = len(original_waypoints) // 2
        ax.plot(modified_waypoints[mid_idx, 0], modified_waypoints[mid_idx, 1], 'k*', 
               markersize=10, label='Modified point')
        
        ax.set_title(f"{method} interpolation")
        ax.grid(True)
        ax.set_aspect('equal')
        
        if i == 0:
            ax.legend()
    
    plt.tight_layout()
    plt.show()
    
    return fig

def plot_density_comparison(methods, waypoints_sets, density_results):
    """Visualize how each method performs with different waypoint densities."""
    density_factors = sorted(list(waypoints_sets.keys()))
    num_methods = len(methods)
    
    fig, axes = plt.subplots(num_methods, len(density_factors), figsize=(15, 12))
    
    # Plot each method
    for i, method in enumerate(methods):
        for j, factor in enumerate(density_factors):
            ax = axes[i, j]
            
            # Plot waypoints
            waypoints = waypoints_sets[factor]
            ax.plot(waypoints[:, 0], waypoints[:, 1], 'ro', markersize=6, label='Waypoints')
            
            # Plot path
            path = density_results[method][factor]
            ax.plot(path[:, 0], path[:, 1], 'b-', linewidth=2)
            
            ax.set_title(f"{method}, density={factor:.1f}x\n({len(waypoints)} points)")
            ax.grid(True)
            ax.set_aspect('equal')
            
            # Remove ticks for cleaner look
            ax.set_xticks([])
            ax.set_yticks([])
    
    plt.tight_layout()
    plt.show()
    
    return fig