import numpy as np
from scipy.optimize import linprog
import plotly.graph_objects as go

# Objective function coefficients (negated for maximization)
c = [-(250 - 130), -(460 - 270), -(550 - 310)]

# Coefficients of constraints
A = [
    [0, 5, 0],    # Specialist labor
    [1, 1, 3],    # Raw material A
    [2, 2, 1],    # Raw material B
    [2, 1, 1]     # Storage volume
]

# Right-hand side of constraints
b = [40, 200, 110, 200]

# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')

# Check if a solution was found
if result.success:
    optimal_value = -result.fun
    optimal_solution = result.x
    print(f"Optimal value: {optimal_value}")
    print(f"Values of decision variables: {optimal_solution}")
else:
    print("No solution found")

# Define the range for x1, x2, x3 with higher density
x1 = np.linspace(0, 100, 100)
x2 = np.linspace(0, 20, 200)
x3 = np.linspace(0, 100, 100)

# Create a grid of points
X1, X2, X3 = np.meshgrid(x1, x2, x3)

# Define the constraints
constraint1 = (0 * X1 + 5 * X2 + 0 * X3 <= 40)
constraint2 = (1 * X1 + 1 * X2 + 3 * X3 <= 200)
constraint3 = (2 * X1 + 2 * X2 + 1 * X3 <= 110)
constraint4 = (2 * X1 + 1 * X2 + 1 * X3 <= 200)

# Combine all constraints
constraints = constraint1 & constraint2 & constraint3 & constraint4

# Select points that satisfy all constraints
x1_feasible = X1[constraints]
x2_feasible = X2[constraints]
x3_feasible = X3[constraints]

# Create the 3D scatter plot for the feasible region with higher density
fig = go.Figure(data=[go.Scatter3d(
    x=x1_feasible,
    y=x2_feasible,
    z=x3_feasible,
    mode='markers',
    marker=dict(size=2, color='purple', opacity=0.5),
    name='Feasible Region'
)])

# Add the optimal solution point
fig.add_trace(go.Scatter3d(
    x=[optimal_solution[0]],
    y=[optimal_solution[1]],
    z=[optimal_solution[2]],
    mode='markers',
    marker=dict(size=5, color='red'),
    name='Optimal Solution'
))

# Update the layout
fig.update_layout(
    title='Linear Programming with Multiple Constraints and Intersections',
    scene=dict(
        xaxis_title='x1',
        yaxis_title='x2',
        zaxis_title='x3',
    ),
    showlegend=True
)

# Show the plot
fig.show()
