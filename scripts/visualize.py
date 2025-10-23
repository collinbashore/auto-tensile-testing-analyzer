import matplotlib.pyplot as plt

def plot_engineering_true_combined_subplots(df, material_name='Material'):
    """
    Plots three subplots:
    1. Engineering stress-strain curve
    2. True stress-strain curve
    3. Combined engineering + true stress-strain curve
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame that contains:
        - 'Engineering Strain'
        - 'Engineering Stress (MPa)'
        - 'True Strain'
        - 'True Stress (MPa)'

    material_name : str, optional
        The name of the material for plot titles and legends.
    """

    # Create 3 horizontal subplots (1 row x 3 columns), with a wide figure size (in inches)
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # Add a main title for the entire figure
    fig.suptitle(f"Stress-Strain Curves for {material_name}", fontsize=14)

    # Subplot 1: Engineering Stress-Strain curve
    axs[0].plot( # Plot on the first axis (axs[0])
        df['Engineering Strain'],
        df['Engineering Stress (MPa)'],
        label='Engineering Curve', # legend label
        color='tab:blue' # line color
    )
    axs[0].set_title('Engineering Stress-Strain') # subplot title
    axs[0].set_xlabel('Engineering Strain')       # x-axis label
    axs[0].set_ylabel('Engineering Stress (MPa)') # y-axis label
    axs[0].grid(True)                             # Add gridlines
    axs[0].legend()                               # Show legend

    # Subplot 2: True Stress-Strain curve
    axs[1].plot(
        df['True Strain'],
        df['True Stress (MPa)'],
        label='True Curve',
        color='tab:red'
    )
    axs[1].set_title('True Stress-Strain')
    axs[1].set_xlabel('True Strain')
    axs[1].set_ylabel('True Stress (MPa)')
    axs[1].grid(True)
    axs[1].legend()

    # Subplot 3: Combined Stress-Strain curves
    axs[2].plot(
        df['Engineering Strain'],
        df['Engineering Stress (MPa)'],
        label='Engineering',
        color='tab:blue'
    )
    axs[2].plot(
        df['True Strain'],
        df['True Stress (MPa)'],
        label='True',
        color='tab:red'
    )
    axs[2].set_title('Engineering vs. True Stress-Strain')
    axs[2].set_xlabel('Strain')
    axs[2].set_ylabel('Stress (MPa)')
    axs[2].grid(True)
    axs[2].legend()

    # Adjust layout to make room for titles and avoid overlaps
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 
    
    # rect parameter leaves space for suptitle, where rect=[left, bottom, right, top]

    # Display the plot window
    plt.show()