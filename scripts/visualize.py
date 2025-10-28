# Stress–strain visualization: plots engineering, true, and combined curves,
# with optional annotations.

import matplotlib.pyplot as plt
from scripts.extract_properties import extract_properties


def plot_engineering_true_combined_subplots(
        df, material_name='Material', props=None):
    """
    A function that plots three subplots:
        1. Engineering stress-strain curve
        2. True stress-strain curve
        3. Combined engineering + true stress-strain curve

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame that contains:
        - 'Engineering Strain'
        - 'Engineering Stress (GPa)'
        - 'True Strain'
        - 'True Stress (GPa)'

    material_name : str, optional
        The name of the material for plot titles and legends.
    props : dict
        A dictionary of extracted properties to annotate the plots.
        If None, properties will be automatically extracted from df.
    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object containing the subplots.
    """

    # Auto-generate properties if not provided
    if props is None:
        props_df = extract_properties(df, material_name)
        props = props_df.iloc[0].to_dict()  # Convert DataFrame row to dictionary for compatibility

    # Figure: 1×3 subplots (wide layout) with better spacing
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    plt.subplots_adjust(wspace=0.3)  # Add more space between subplots

    # Add a main title for the entire figure
    fig.suptitle(f"Stress-Strain Curves for {material_name}", fontsize=14)

    # Subplot 1: Engineering Stress-Strain curve
    axs[0].plot(  # Plot on the first axis (axs[0])
        df['Engineering Strain'],
        df['Engineering Stress (GPa)'],
        label='Engineering Curve',  # legend label
        color='tab:blue'  # line color
    )
    axs[0].set_title('Engineering Stress-Strain')  # subplot title
    axs[0].set_xlabel('Engineering Strain')        # x-axis label
    axs[0].set_ylabel('Engineering Stress (GPa)')  # y-axis label
    axs[0].grid(True)                              # Add gridlines

    # Subplot 2: True Stress-Strain curve
    axs[1].plot(
        df['True Strain'],
        df['True Stress (GPa)'],
        label='True Curve',
        color='tab:red'
    )
    axs[1].set_title('True Stress-Strain')
    axs[1].set_xlabel('True Strain')
    axs[1].set_ylabel('True Stress (GPa)')
    axs[1].grid(True)

    # Subplot 3: Combined Stress-Strain curves
    axs[2].plot(
        df['Engineering Strain'],
        df['Engineering Stress (GPa)'],
        label='Engineering',
        color='tab:blue'
    )
    axs[2].plot(
        df['True Strain'],
        df['True Stress (GPa)'],
        label='True',
        color='tab:red'
    )
    axs[2].set_title('Engineering vs. True Stress-Strain')
    axs[2].set_xlabel('Strain')
    axs[2].set_ylabel('Stress (GPa)')
    axs[2].grid(True)

    # ============================================================================
    # ADD LABELS AND ANNOTATIONS TO THE PLOTS
    # ============================================================================
    # This section adds helpful labels, lines, and text boxes to point out
    # important features in the stress-strain curves (like where the material
    # starts to yield, where it reaches maximum strength, etc.)

    if props:  # Only add annotations if we have material properties to display

        # STEP 1: Find the highest and lowest values in our data
        # ---------------------------------------------------------------
        # Think of this like finding the "edges" of our graph so we know
        # where to place labels without them going off the chart or
        # overlapping data

        eng_y_min, eng_y_max = (df['Engineering Stress (GPa)'].min(),
                                df['Engineering Stress (GPa)'].max())
        eng_x_min, eng_x_max = (df['Engineering Strain'].min(),
                                df['Engineering Strain'].max())
        true_y_min, true_y_max = (df['True Stress (GPa)'].min(),
                                  df['True Stress (GPa)'].max())
        true_x_min, true_x_max = (df['True Strain'].min(),
                                  df['True Strain'].max())

        # STEP 2: Calculate smart spacing for our labels
        # ---------------------------------------------------------------
        # Instead of using fixed distances (like "10 units to the right")
        # we calculate spacing as a small percentage (2.5%) of the total
        # range. This way, labels always look good no matter how big or
        # small our numbers are.

        # Calculate spacing for labels (only what we need for cleaner plots)
        eng_y_offset = (eng_y_max - eng_y_min) * 0.025
        true_y_offset = (true_y_max - true_y_min) * 0.025

        # ================================================================
        # ANNOTATE THE ENGINEERING STRESS-STRAIN PLOT (Left subplot)
        # ================================================================

        # Mark the YIELD STRENGTH (where permanent deformation begins)
        # ------------------------------------------------------------
        # Convert properties from MPa to GPa for plotting consistency
        yield_strength_gpa = props['Yield Strength (MPa)'] / 1000
        uts_gpa = props['Ultimate Tensile Strength (UTS, MPa)'] / 1000
        
        # Add clean horizontal lines for key stress levels
        axs[0].axhline(yield_strength_gpa, color='green',
                       linestyle='--', linewidth=1.2, alpha=0.8)
        axs[0].axhline(uts_gpa, color='orange',
                       linestyle='--', linewidth=1.2, alpha=0.8)

        # Add simple text labels positioned to avoid overlap
        # Place yield label on the left side
        axs[0].text(eng_x_max * 0.02, yield_strength_gpa + eng_y_offset * 0.5,
                   f'Yield: {yield_strength_gpa:.3f} GPa',
                   color='green', fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Place UTS label on the right side to avoid overlap
        axs[0].text(eng_x_max * 0.65, uts_gpa + eng_y_offset * 0.5,
                   f'UTS: {uts_gpa:.3f} GPa',
                   color='orange', fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

        # Mark the FRACTURE POINT with a simple vertical line
        axs[0].axvline(props['Fracture Strain'], color='purple',
                       linestyle='--', linewidth=1.2, alpha=0.8)
        
        # Add simple fracture label at bottom
        axs[0].text(props['Fracture Strain'], eng_y_max * 0.05,
                   f'Fracture\nε = {props["Fracture Strain"]:.3f}',
                   color='purple', fontsize=8, fontweight='bold',
                   ha='center', va='bottom',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

        # Create a SUMMARY BOX with key material properties
        # ------------------------------------------------------------
        # This creates a neat text box in the upper-right corner that
        # displays the most important properties all in one place
        # (like a "stats card")
        #
        # The \.format or f-string {:.2f} means "show 2 decimal places"
        # The \n creates new lines between each property
        # The ━ characters create a visual separator line

        # Simplified material properties box
        props_text = (
            f"Material Properties:\n"
            f"E: {props['Elastic Modulus (GPa)']:.1f} GPa\n"
            f"Elongation: {props['Percent Elongation (%)']:.1f}%"
        )

        # Place a smaller, cleaner text box in upper-right
        axs[0].text(
            0.98, 0.98, props_text,
            transform=axs[0].transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightblue',
                      edgecolor='darkblue', alpha=0.85, linewidth=1)
        )

        # ================================================================
        # ANNOTATE THE TRUE STRESS-STRAIN PLOT (Middle subplot)
        # ================================================================
        # True stress-strain accounts for the changing cross-sectional
        # area as the material stretches (engineering stress assumes
        # constant area)

        # Add clean reference lines for True Stress plot
        true_stress_uts_gpa = props['True Stress at UTS (GPa)']
        axs[1].axhline(true_stress_uts_gpa, color='orange',
                       linestyle='--', linewidth=1.2, alpha=0.8)
        axs[1].axvline(props['Necking Strain'], color='purple',
                       linestyle='--', linewidth=1.2, alpha=0.8)

        # Add simple labels positioned to avoid overlap
        axs[1].text(true_x_max * 0.02, true_stress_uts_gpa + true_y_offset * 0.5,
                   f'True Stress at UTS\n{true_stress_uts_gpa:.3f} GPa',
                   color='orange', fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        axs[1].text(props['Necking Strain'], true_y_max * 0.05,
                   f'Necking Point\nε = {props["Necking Strain"]:.3f}',
                   color='purple', fontsize=8, fontweight='bold',
                   ha='center', va='bottom',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

        # Simplified properties box for True Stress plot
        true_props_text = (
            f"True Strain Analysis:\n"
            f"Necking: {props['Necking Strain']:.3f}\n"
            f"Area Reduction: {props['Percent Reduction in Area (%)']:.1f}%"
        )

        axs[1].text(
            0.98, 0.98, true_props_text,
            transform=axs[1].transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4',
                      facecolor='lightyellow',
                      alpha=0.85, linewidth=1)
        )

    # ====================================================================
    # ADD LEGENDS TO ALL THREE SUBPLOTS
    # ====================================================================
    # Legends show what each line/color represents on the graph
    # - loc='upper left' puts the legend in the top-left corner
    # - framealpha=0.9 makes the legend box mostly opaque
    # - edgecolor='black' gives the legend box a black border

    axs[0].legend(loc='upper left', framealpha=0.9, edgecolor='black',
                  fontsize=9)
    axs[1].legend(loc='upper left', framealpha=0.9, edgecolor='black',
                  fontsize=9)
    axs[2].legend(loc='upper left', framealpha=0.9, edgecolor='black',
                  fontsize=9)

    # Tight layout to neatly arrange subplots and avoid overlap
    # Reserve 3% bottom and 5% top margins for labels/title
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Show plots
    plt.show()

    # Return figure for saving or further use
    return fig
