import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored

# Import interpolation methods
from interpolation import (
    newton_interpolate,
    lagrange_interpolate, 
    cubic_spline_interpolate,
    b_spline_interpolate
)

# Import utilities
from utils.waypoints import (
    get_test_waypoints,
    generate_random_waypoints,
    generate_waypoints_with_density
)
from utils.metrics import compare_methods
from utils.visualization import (
    plot_interpolation_comparison,
    plot_curvature_comparison,
    plot_local_control_effect,
    plot_density_comparison
)
from utils.testing import run_method_tests
from simulation.physics import calculate_curvature

class ProjectRunner:
    def __init__(self):
        self.results = {}
        self.current_waypoints = None
        self.waypoint_name = None
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self):
        print(colored("\n==== Numerical Methods: Path Smoothing Project ====", "cyan", attrs=["bold"]))
        print(colored("This tool helps you test and analyze your interpolation implementations\n", "cyan"))
        
    def main_menu(self):
        while True:
            self.clear_screen()
            self.print_header()
            
            print("1. Test your implementations")
            print("2. Select waypoints")
            print("3. Run comparative experiments")
            print("4. Visualize individual method")
            print("5. Generate report data")
            print("6. Exit")
            
            choice = input("\nEnter your choice [1-6]: ")
            
            if choice == '1':
                self.test_implementations()
            elif choice == '2':
                self.select_waypoints()
            elif choice == '3':
                self.run_experiments()
            elif choice == '4':
                self.visualize_method()
            elif choice == '5':
                self.generate_report()
            elif choice == '6':
                print("Exiting program. Goodbye!")
                sys.exit(0)
            else:
                input("Invalid choice. Press Enter to continue...")
    
    def test_implementations(self):
        self.clear_screen()
        print(colored("Testing your interpolation implementations...", "yellow"))
        print("This will check if your implementations are mathematically correct.\n")
        
        methods = ['newton', 'lagrange', 'cubic_spline', 'b_spline']
        all_passed = True
        
        for method in methods:
            print(f"Testing {method.upper()} interpolation...")
            passed, results = run_method_tests(method)
            
            if passed:
                print(colored(f"✓ {method.upper()} tests PASSED!", "green"))
            else:
                print(colored(f"✗ {method.upper()} tests FAILED!", "red"))
                all_passed = False
                for test_name, result in results.items():
                    if not result['passed']:
                        print(f"  - {test_name}: {result['error_message']}")
            print()
        
        if all_passed:
            print(colored("Congratulations! All implementations passed the tests.", "green", attrs=["bold"]))
        else:
            print(colored("Some implementations failed. Please fix the issues and try again.", "yellow"))
        
        input("\nPress Enter to return to main menu...")
    
    def select_waypoints(self):
        self.clear_screen()
        print(colored("Select waypoints for experiments:", "yellow"))
        print("These waypoints will be used for visualization and experiments.\n")
        
        print("Available waypoint sets:")
        print("1. Simple curve (3 points)")
        print("2. Complex path (5 points)")
        print("3. Zigzag path (7 points)")
        print("4. Sharp turns (7 points)")
        print("5. Circle (8 points)")
        print("6. Random waypoints")
        print("7. Return to main menu")
        
        choice = input("\nEnter your choice [1-7]: ")
        
        if choice == '1':
            self.waypoint_name = 'simple_curve'
        elif choice == '2':
            self.waypoint_name = 'complex'
        elif choice == '3':
            self.waypoint_name = 'zigzag'
        elif choice == '4':
            self.waypoint_name = 'sharp_turns'
        elif choice == '5':
            self.waypoint_name = 'circle'
        elif choice == '6':
            self.waypoint_name = 'random'
            num_points = int(input("Enter number of random points [3-10]: "))
            self.current_waypoints = generate_random_waypoints(min(max(num_points, 3), 10))
            input("\nRandom waypoints generated. Press Enter to continue...")
            return
        elif choice == '7':
            return
        else:
            input("Invalid choice. Press Enter to try again...")
            self.select_waypoints()
            return
        
        self.current_waypoints = get_test_waypoints(self.waypoint_name)
        
        # Visualize selected waypoints
        plt.figure(figsize=(8, 6))
        plt.plot(self.current_waypoints[:, 0], self.current_waypoints[:, 1], 'ro-')
        plt.title(f"Selected Waypoints: {self.waypoint_name}")
        plt.grid(True)
        plt.axis('equal')
        plt.show()
        
        input("\nWaypoints selected. Press Enter to continue...")
    
    def run_experiments(self):
        if self.current_waypoints is None:
            input("Please select waypoints first. Press Enter to continue...")
            return
            
        self.clear_screen()
        print(colored("Available Experiments:", "yellow"))
        print("1. Accuracy vs. Smoothness")
        print("2. Local Control Properties")
        print("3. Waypoint Density Analysis")
        print("4. Return to main menu")
        
        choice = input("\nEnter your choice [1-4]: ")
        
        if choice == '1':
            self.experiment_accuracy_smoothness()
        elif choice == '2':
            self.experiment_local_control()
        elif choice == '3':
            self.experiment_density()
        elif choice == '4':
            return
        else:
            input("Invalid choice. Press Enter to try again...")
            self.run_experiments()
    
    def experiment_accuracy_smoothness(self):
        self.clear_screen()
        print(colored("Experiment: Accuracy vs. Smoothness", "yellow"))
        print("This experiment shows how each method balances accuracy and smoothness.\n")
        
        # Get paths and curvatures for each method
        methods = ['newton', 'lagrange', 'cubic_spline', 'b_spline']
        paths = {}
        curvatures = {}
        
        for method in methods:
            print(f"Running {method} interpolation...")
            # Call the appropriate interpolation function
            if method == 'newton':
                paths[method] = newton_interpolate(self.current_waypoints)
            elif method == 'lagrange':
                paths[method] = lagrange_interpolate(self.current_waypoints)
            elif method == 'cubic_spline':
                paths[method] = cubic_spline_interpolate(self.current_waypoints)
            elif method == 'b_spline':
                paths[method] = b_spline_interpolate(self.current_waypoints)
        
        # Get comparison metrics
        from simulation.physics import calculate_curvature
        for method in methods:
            path = paths[method]
            curvatures[method] = calculate_curvature(path[:, 0], path[:, 1])
        
        # Plot comparison
        plot_interpolation_comparison(self.current_waypoints, paths)
        plot_curvature_comparison(paths, curvatures)
        
        # Calculate and display metrics
        comparison = compare_methods(self.current_waypoints, paths)
        
        print("\nComparison Metrics:")
        print("------------------")
        print(f"{'Method':<15} {'Path Length':<12} {'Max Dev':<10} {'Mean Dev':<10} {'Max Curv':<10}")
        print("-" * 60)
        
        for method in methods:
            metrics = comparison[method]
            print(f"{method:<15} {metrics['path_length']:<12.2f} {metrics['max_deviation']:<10.2f} "
                  f"{metrics['mean_deviation']:<10.2f} {metrics['max_curvature']:<10.4f}")
        
        self.results['accuracy_smoothness'] = {
            'paths': paths,
            'curvatures': curvatures,
            'metrics': comparison
        }
        
        print("\nObservations to note:")
        print("1. Which method produces the smoothest path? (lowest max curvature)")
        print("2. Which method follows the waypoints most accurately? (lowest deviation)")
        print("3. Do you notice any trade-offs between smoothness and accuracy?")
        
        input("\nPress Enter to return to experiments menu...")
    
    def experiment_local_control(self):
        self.clear_screen()
        print(colored("Experiment: Local Control Properties", "yellow"))
        print("This experiment shows how changing one waypoint affects the entire curve.\n")
        
        # Create modified waypoints with one point moved
        modified_waypoints = self.current_waypoints.copy()
        mid_idx = len(modified_waypoints) // 2
        modified_waypoints[mid_idx, 1] += 50  # Move middle point up
        
        methods = ['newton', 'lagrange', 'cubic_spline', 'b_spline']
        original_paths = {}
        modified_paths = {}
        
        for method in methods:
            print(f"Running {method} interpolation...")
            # Original path
            if method == 'newton':
                original_paths[method] = newton_interpolate(self.current_waypoints)
                modified_paths[method] = newton_interpolate(modified_waypoints)
            elif method == 'lagrange':
                original_paths[method] = lagrange_interpolate(self.current_waypoints)
                modified_paths[method] = lagrange_interpolate(modified_waypoints)
            elif method == 'cubic_spline':
                original_paths[method] = cubic_spline_interpolate(self.current_waypoints)
                modified_paths[method] = cubic_spline_interpolate(modified_waypoints)
            elif method == 'b_spline':
                original_paths[method] = b_spline_interpolate(self.current_waypoints)
                modified_paths[method] = b_spline_interpolate(modified_waypoints)
        
        # Plot results
        plot_local_control_effect(methods, self.current_waypoints, modified_waypoints, 
                                  original_paths, modified_paths)
        
        # Calculate and display metrics
        print("\nCalculating change metrics...")
        change_metrics = {}
        
        for method in methods:
            orig = original_paths[method]
            mod = modified_paths[method]
            
            # Calculate average change in path positions
            changes = np.linalg.norm(orig - mod, axis=1)
            avg_change = np.mean(changes)
            max_change = np.max(changes)
            
            # Calculate percentage of path that changed significantly
            significant_threshold = 5.0  # Consider changes > 5 units as significant
            significant_percent = np.sum(changes > significant_threshold) / len(changes) * 100
            
            change_metrics[method] = {
                'avg_change': avg_change,
                'max_change': max_change,
                'significant_percent': significant_percent
            }
        
        # Display metrics
        print("\nLocal Control Metrics:")
        print("--------------------")
        print(f"{'Method':<15} {'Avg Change':<12} {'Max Change':<12} {'% Significant':<15}")
        print("-" * 57)
        
        for method in methods:
            metrics = change_metrics[method]
            print(f"{method:<15} {metrics['avg_change']:<12.2f} {metrics['max_change']:<12.2f} "
                  f"{metrics['significant_percent']:<15.2f}")
        
        self.results['local_control'] = {
            'original_paths': original_paths,
            'modified_paths': modified_paths,
            'metrics': change_metrics
        }
        
        print("\nObservations to note:")
        print("1. Which methods show more local control? (changes confined to area near modified point)")
        print("2. Which methods have changes that affect the entire curve?")
        print("3. How does this relate to the mathematical formulation of each method?")
        
        input("\nPress Enter to return to experiments menu...")


    def experiment_density(self):
        self.clear_screen()
        print(colored("Experiment: Waypoint Density Analysis", "yellow"))
        print("This experiment shows how each method performs with different waypoint densities.\n")
        
        # Get base waypoints
        base_waypoints = self.current_waypoints
        
        # Generate different density waypoints
        density_factors = [0.5, 1.0, 2.0]
        waypoints_sets = {}
        
        for factor in density_factors:
            if factor == 1.0:
                waypoints_sets[factor] = base_waypoints
            else:
                waypoints_sets[factor] = generate_waypoints_with_density(base_waypoints, factor)
            print(f"Generated waypoints with density factor {factor} "
                  f"({len(waypoints_sets[factor])} points)")
        
        # Run interpolation for each method and density
        methods = ['newton', 'lagrange', 'cubic_spline', 'b_spline']
        density_results = {}
        
        for method in methods:
            density_results[method] = {}
            print(f"\nRunning {method} interpolation for different densities...")
            
            for factor in density_factors:
                waypoints = waypoints_sets[factor]
                
                # Call the appropriate interpolation function
                if method == 'newton':
                    path = newton_interpolate(waypoints)
                elif method == 'lagrange':
                    path = lagrange_interpolate(waypoints)
                elif method == 'cubic_spline':
                    path = cubic_spline_interpolate(waypoints)
                elif method == 'b_spline':
                    path = b_spline_interpolate(waypoints)
                
                density_results[method][factor] = path
        
        # Plot results
        plot_density_comparison(methods, waypoints_sets, density_results)
        
        # Calculate and display metrics
        print("\nWaypoint Density Analysis:")
        print("------------------------")
        print("Path length for different density factors:")
        print(f"{'Method':<15} {'0.5x Density':<15} {'1.0x Density':<15} {'2.0x Density':<15}")
        print("-" * 63)
        
        for method in methods:
            lengths = [np.sum(np.sqrt(np.sum(np.diff(density_results[method][f], axis=0)**2, axis=1))) 
                      for f in density_factors]
            print(f"{method:<15} {lengths[0]:<15.2f} {lengths[1]:<15.2f} {lengths[2]:<15.2f}")
        
        self.results['density'] = {
            'waypoints_sets': waypoints_sets,
            'paths': density_results
        }
        
        print("\nObservations to note:")
        print("1. Which methods are most sensitive to changes in waypoint density?")
        print("2. Which methods maintain smoothness even with sparse waypoints?")
        print("3. Do any methods behave erratically with certain density configurations?")
        
        input("\nPress Enter to return to experiments menu...")
    
    def visualize_method(self):
        if self.current_waypoints is None:
            input("Please select waypoints first. Press Enter to continue...")
            return
            
        self.clear_screen()
        print(colored("Visualize Individual Method:", "yellow"))
        print("1. Newton interpolation")
        print("2. Lagrange interpolation")
        print("3. Cubic spline interpolation")
        print("4. B-spline interpolation")
        print("5. Return to main menu")
        
        choice = input("\nEnter your choice [1-5]: ")
        
        if choice == '5':
            return
            
        if choice not in ['1', '2', '3', '4']:
            input("Invalid choice. Press Enter to try again...")
            self.visualize_method()
            return
        
        method_idx = int(choice) - 1
        method_names = ['newton', 'lagrange', 'cubic_spline', 'b_spline']
        method = method_names[method_idx]
        
        self.clear_screen()
        print(f"Visualizing {method} interpolation for {self.waypoint_name} waypoints...")
        
        # Run interpolation
        if method == 'newton':
            path = newton_interpolate(self.current_waypoints)
        elif method == 'lagrange':
            path = lagrange_interpolate(self.current_waypoints)
        elif method == 'cubic_spline':
            path = cubic_spline_interpolate(self.current_waypoints)
        elif method == 'b_spline':
            path = b_spline_interpolate(self.current_waypoints)
            
        # Calculate curvature
        curvature = calculate_curvature(path[:, 0], path[:, 1])
        
        # Plot results
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Path plot
        ax1.plot(self.current_waypoints[:, 0], self.current_waypoints[:, 1], 'ro-', label='Waypoints')
        ax1.plot(path[:, 0], path[:, 1], 'b-', label=f'{method} interpolation')
        ax1.set_title(f'{method} interpolation path')
        ax1.grid(True)
        ax1.legend()
        ax1.set_aspect('equal')
        
        # Curvature plot
        ax2.plot(range(len(curvature)), curvature)
        ax2.set_title(f'Curvature profile (max: {np.max(curvature):.4f})')
        ax2.grid(True)
        ax2.set_xlabel('Path point index')
        ax2.set_ylabel('Curvature')
        
        plt.tight_layout()
        plt.show()
        
        input("\nPress Enter to return to main menu...")
    
    def generate_report(self):
        self.clear_screen()
        
        if not self.results:
            print(colored("No experiment results found.", "yellow"))
            print("Please run some experiments first.")
            input("\nPress Enter to return to main menu...")
            return
        
        print(colored("Generating Report Data", "yellow"))
        print("This will create a CSV file with metrics and save plots for your report.\n")
        
        # Create output directory
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"report_data_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save experiment results
        if 'accuracy_smoothness' in self.results:
            print("Saving accuracy vs. smoothness results...")
            metrics = self.results['accuracy_smoothness']['metrics']
            
            with open(f"{output_dir}/accuracy_smoothness.csv", 'w') as f:
                f.write("Method,PathLength,MaxDeviation,MeanDeviation,MaxCurvature\n")
                for method, m in metrics.items():
                    f.write(f"{method},{m['path_length']:.4f},{m['max_deviation']:.4f},"
                           f"{m['mean_deviation']:.4f},{m['max_curvature']:.4f}\n")
            
            # Save plot
            fig = plot_interpolation_comparison(self.current_waypoints, 
                                              self.results['accuracy_smoothness']['paths'])
            fig.savefig(f"{output_dir}/accuracy_smoothness_paths.png", dpi=300)
            plt.close(fig)
            
            fig = plot_curvature_comparison(self.results['accuracy_smoothness']['paths'], 
                                          self.results['accuracy_smoothness']['curvatures'])
            fig.savefig(f"{output_dir}/accuracy_smoothness_curvatures.png", dpi=300)
            plt.close(fig)
        
        if 'local_control' in self.results:
            print("Saving local control results...")
            metrics = self.results['local_control']['metrics']
            
            with open(f"{output_dir}/local_control.csv", 'w') as f:
                f.write("Method,AvgChange,MaxChange,SignificantPercent\n")
                for method, m in metrics.items():
                    f.write(f"{method},{m['avg_change']:.4f},{m['max_change']:.4f},"
                           f"{m['significant_percent']:.4f}\n")
        
        if 'density' in self.results:
            print("Saving density analysis results...")
            
            # Calculate path lengths
            methods = ['newton', 'lagrange', 'cubic_spline', 'b_spline']
            density_factors = [0.5, 1.0, 2.0]
            
            with open(f"{output_dir}/density_analysis.csv", 'w') as f:
                f.write("Method,Density0.5,Density1.0,Density2.0\n")
                
                for method in methods:
                    lengths = [np.sum(np.sqrt(np.sum(np.diff(self.results['density']['paths'][method][f], 
                                                           axis=0)**2, axis=1))) 
                              for f in density_factors]
                    f.write(f"{method},{lengths[0]:.4f},{lengths[1]:.4f},{lengths[2]:.4f}\n")
        
        print(f"\nReport data saved to {output_dir}/")
        print("You can use these files in your project report.")
        
        input("\nPress Enter to return to main menu...")


if __name__ == '__main__':
    app = ProjectRunner()
    app.main_menu()