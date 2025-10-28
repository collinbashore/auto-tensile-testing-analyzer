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

    # Figure: 1×3 subplots (wide layout)
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

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

        # 2.5% of vertical/horizontal range
        eng_y_offset = (eng_y_max - eng_y_min) * 0.025
        eng_x_offset = (eng_x_max - eng_x_min) * 0.025
        true_y_offset = (true_y_max - true_y_min) * 0.025
        true_x_offset = (true_x_max - true_x_min) * 0.025

        # STEP 3: Create a consistent style for all text labels
        # ---------------------------------------------------------------
        # This is like creating a "template" for how all our labels
        # should look:
        # - Small but readable font (size 9)
        # - Bold text so it stands out
        # - White background box with gray border (makes text easier to
        #   read)
        # - Slightly transparent (alpha=0.85) so it doesn't completely
        #   hide the graph

        text_style = {
            'fontsize': 9,
            'fontweight': 'bold',
            'bbox': dict(boxstyle='round,pad=0.4', facecolor='white',
                         edgecolor='gray', alpha=0.85)
        }

        # ================================================================
        # ANNOTATE THE ENGINEERING STRESS-STRAIN PLOT (Left subplot)
        # ================================================================

        # Mark the YIELD STRENGTH (where permanent deformation begins)
        # ------------------------------------------------------------
        # 1. Draw a horizontal green dashed line across the plot at the
        #    yield stress level
        axs[0].axhline(props['Yield Strength (MPa)'], color='green',
                       linestyle='--', linewidth=1.5, alpha=0.7)

        # 2. Add a label with an arrow pointing to this line
        #    - xy = where the arrow points TO (the actual yield point
        #      on the graph)
        #    - xytext = where the text box appears
        #    - The "\n" creates a line break to show the value below
        #      the label
        axs[0].annotate(
            f"Yield\n{props['Yield Strength (MPa)']:.1f} MPa",
            xy=(eng_x_max * 0.05, props['Yield Strength (MPa)']),
            xytext=(eng_x_max * 0.15,
                    props['Yield Strength (MPa)'] + eng_y_offset * 2),
            arrowprops=dict(arrowstyle='->', color='green', lw=1.2),
            color='green', **text_style
        )

        # Mark the ULTIMATE TENSILE STRENGTH / UTS (maximum stress
        # before failure)
        # ------------------------------------------------------------
        # Same process as above, but for the maximum strength point
        # (in orange)
        axs[0].axhline(props['Ultimate Tensile Strength (UTS, MPa)'],
                       color='orange', linestyle='--', linewidth=1.5,
                       alpha=0.7)
        axs[0].annotate(
            f"UTS\n{props['Ultimate Tensile Strength (UTS, MPa)']:.1f} "
            f"MPa",
            xy=(eng_x_max * 0.05,
                props['Ultimate Tensile Strength (UTS, MPa)']),
            xytext=(eng_x_max * 0.15,
                    props['Ultimate Tensile Strength (UTS, MPa)']
                    + eng_y_offset * 2),
            arrowprops=dict(arrowstyle='->', color='orange', lw=1.2),
            color='orange', **text_style
        )

        # Mark the FRACTURE POINT (where the material breaks)
        # ------------------------------------------------------------
        # This time we draw a VERTICAL line (axvline) because fracture
        # is about how much the material stretched (strain on x-axis),
        # not stress level
        axs[0].axvline(props['Fracture Strain'], color='purple',
                       linestyle='--', linewidth=1.5, alpha=0.7)
        axs[0].annotate(
            f"Fracture\nε = {props['Fracture Strain']:.3f}",
            xy=(props['Fracture Strain'], eng_y_max * 0.3),
            xytext=(props['Fracture Strain'] - eng_x_offset * 3,
                    eng_y_max * 0.4),
            arrowprops=dict(arrowstyle='->', color='purple', lw=1.2),
            color='purple', **text_style
        )

        # Create a SUMMARY BOX with key material properties
        # ------------------------------------------------------------
        # This creates a neat text box in the upper-right corner that
        # displays the most important properties all in one place
        # (like a "stats card")
        #
        # The \.format or f-string {:.2f} means "show 2 decimal places"
        # The \n creates new lines between each property
        # The ━ characters create a visual separator line

        props_text = (
            f"Material Properties:\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Resilience: {props['Resilience (MPa)']:.2f} MPa\n"
            f"Toughness: {props['Toughness (MPa)']:.2f} MPa\n"
            f"Elastic Modulus: "
            f"{props['Elastic Modulus (GPa)']:.2f} GPa\n"
            f"% Elongation: {props['Percent Elongation (%)']:.1f}%"
        )

        # Place the text box using "axis coordinates"
        # (transform=axs[0].transAxes)
        # This means (0.97, 0.97) = 97% to the right, 97% up from
        # bottom-left corner
        # So the box will always be in the upper-right, no matter what
        # our data values are
        axs[0].text(
            0.97, 0.97, props_text,
            transform=axs[0].transAxes,  # Use relative positioning
            verticalalignment='top',  # Align top of text box
            horizontalalignment='right',  # Align right edge of box
            bbox=dict(boxstyle='round,pad=0.6', facecolor='lightblue',
                      edgecolor='darkblue', alpha=0.85, linewidth=1.5),
            fontsize=8.5,
            family='monospace',  # Monospace font makes numbers line up
            fontweight='normal'
        )

        # ================================================================
        # ANNOTATE THE TRUE STRESS-STRAIN PLOT (Middle subplot)
        # ================================================================
        # True stress-strain accounts for the changing cross-sectional
        # area as the material stretches (engineering stress assumes
        # constant area)

        # Mark the TRUE STRESS AT UTS (maximum true stress)
        # ------------------------------------------------------------
        axs[1].axhline(props['True Stress at UTS (MPa)'],
                       color='orange', linestyle='--', linewidth=1.5,
                       alpha=0.7)
        axs[1].annotate(
            f"True Stress at UTS\n"
            f"{props['True Stress at UTS (MPa)']:.1f} MPa",
            xy=(true_x_max * 0.05, props['True Stress at UTS (MPa)']),
            xytext=(true_x_max * 0.2,
                    props['True Stress at UTS (MPa)']
                    + true_y_offset * 2),
            arrowprops=dict(arrowstyle='->', color='orange', lw=1.2),
            color='orange', **text_style
        )

        # Mark the NECKING POINT (where the material starts to narrow
        # / thin out)
        # ------------------------------------------------------------
        # Necking is when a material develops a "neck" or narrow
        # section before breaking
        axs[1].axvline(props['Necking Strain'], color='purple',
                       linestyle='--', linewidth=1.5, alpha=0.7)
        axs[1].annotate(
            f"Necking Point\nε_true = {props['Necking Strain']:.3f}",
            xy=(props['Necking Strain'], true_y_max * 0.5),
            xytext=(props['Necking Strain'] - true_x_offset * 3,
                    true_y_max * 0.6),
            arrowprops=dict(arrowstyle='->', color='purple', lw=1.2),
            color='purple', **text_style
        )

        # Create a SUMMARY BOX for true strain analysis
        # ------------------------------------------------------------
        true_props_text = (
            f"True Strain Analysis:\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Necking Strain: {props['Necking Strain']:.3f}\n"
            f"% Area Reduction: "
            f"{props['Percent Reduction in Area (%)']:.1f}%"
        )

        axs[1].text(
            0.97, 0.97, true_props_text,
            transform=axs[1].transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.6',
                      facecolor='lightyellow',
                      edgecolor='darkorange',
                      alpha=0.85, linewidth=1.5),
            fontsize=8.5,
            family='monospace',
            fontweight='normal'
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
