# Calculating Stress-Strain Curves (Engineering and True)

import numpy as np


def calculate_stress_strain(df, A_0, L_0):
    """
    This function calculates the engineering and true stress-strain values
    based on input tensile data.

    Parameters:
    -----------
    df (pd.DataFrame): Input DataFrame with Force (N) and Elongation (mm).
    A_0 (float): Initial cross-sectional area in mm².
    L_0 (float): Initial gauge length in mm.

    Returns:
    --------
    pd.DataFrame: Updated DataFrame with:
        - Engineering Strain (unitless)
        - Engineering Stress (GPa)
        - True Strain (unitless)
        - True Stress (GPa)
    """
    df = df.copy()  # To avoid modifying the original DataFrame

    # Engineering stress and strain
    # Convert to GPa, where 1 N/mm² = 1 MPa = 1e-3 GPa
    df['Engineering Stress (GPa)'] = (df['Force (N)'] / A_0) * 1e-3
    df['Engineering Strain'] = df['Elongation (mm)'] / L_0

    # True stress and strain
    df['True Strain'] = np.log(1 + df['Engineering Strain'])
    # np.log is the natural logarithm function

    df['True Stress (GPa)'] = (
        df['Engineering Stress (GPa)']
        * (1 + df['Engineering Strain'])
    )

    # Return dataframe with relevant columns only
    df = df[['Engineering Strain', 'Engineering Stress (GPa)',
            'True Strain', 'True Stress (GPa)']]

    return df
