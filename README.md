#  Piecewise Interpolation for Robot Path Planning

**Course:** Numerical Methods in Computer Engineering   
**Department:** Artificial Intelligence and Data Engineering  

---

## Project Description

This project investigates how four popular interpolation methods — **Newton, Lagrange, Cubic Spline, and B-Spline** — perform in robot path planning tasks. Each method was evaluated based on:

-  **Accuracy**
- **Smoothness**
-  **Local Control**
- **Sensitivity to Waypoint Density**

Using a ready-made experimental interface, each method was tested across different path geometries (circle, zigzag, sharp turns), and results were recorded with visualizations and quantitative metrics.

---

##  Methods Compared

| Method         | Type              | Notes |
|----------------|-------------------|-------|
| Newton         | Global polynomial | Efficient for incremental paths but sensitive to noise |
| Lagrange       | Global polynomial | High instability with dense or circular paths |
| Cubic Spline   | Piecewise spline  | Excellent balance of accuracy and smoothness |
| B-Spline       | Approximation     | Superior smoothness and local control, does not pass through all waypoints |

---

##  Key Metrics

- Path Length  
- Max & Mean Deviation  
- Max Curvature  
- % of Path Affected by Local Changes  
- Runtime Stability  

---

##  Experiment Types

1. **Accuracy vs. Smoothness**  
2. **Local Control Sensitivity**  
3. **Waypoint Density Comparison** (sparse, medium, dense)

---

##  Results Summary

-  **Cubic Spline**: Best for practical path planning; smooth and accurate  
-  **B-Spline**: Best smoothness and local control; ideal for animation or soft motion  
-  **Lagrange**: Unstable with dense points (Runge's phenomenon)  
-  **Newton**: Good incrementally, but globally sensitive  

---

##  What I Learned

> "Interpolation methods are not just math—they shape how a robot moves in space. Choosing the wrong one can make a smooth path jittery or unstable."

---


