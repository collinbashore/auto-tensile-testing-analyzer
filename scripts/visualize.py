import matplotlib.pyplot as plt

def plot_stress_strain(df):
    """
    Plots the engineering stress-strain curve using matplotlib.

    Parameters:
    -----------
    df : pd.DataFrame
        A DataFrame that must contain the following two columns:
            - 'Engineering Strain': The strain values (unitless)
            - 'Engineering Stress (MPa)': The corresponding stress values in MPa

    Description:
    ------------
    This function generates a line plot of Engineering Stress (y-axis) vs.
    Engineering Strain (x-axis). It includes:
        - Gridlines
        - Axis labels
        - A plot legend
        - A plot title
        - Tight layout adjustment for better spacing

    Visualization is critical for understanding material behavior. 
    This curve reveals:
        - Elastic behavior (initial linear region)
        - Yield point
        - Plastic deformation (non-linear region)
        - Ultimate tensile strength
        - Fracture point (curve endpoint)

    Returns:
    --------
    None
        Displays the plot using plt.show().
    """
    plt.figure(figsize=(8, 5))
    plt.plot(df['Engineering Strain'], df['Engineering Stress (MPa)'], label='Stress-Strain Curve')
    plt.xlabel('Engineering Strain')
    plt.ylabel('Engineering Stress (MPa)')
    plt.title('Stress-Strain Curve')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()