import pandas as pd

def calculate_engineering_stress_strain(df, A_0, L_0):
    """
    This function calculates the engineering and true stress-strain values based on input tensile data.

    Parameters:
    -----------
    df (pd.DataFrame): Input DataFrame with Force (N) and Elongation (mm).
    A_0 (float): Initial cross-sectional area in mm².
    L_0 (float): Initial gauge length in mm.

    Returns:
    --------
    pd.DataFrame: Updated DataFrame with:
        - Engineering Strain (unitless)
        - Engineering Stress (MPa)
        - True Strain (unitless)
        - True Stress (MPa)
    """
    df = df.copy() # To avoid modifying the original DataFrame
    
    # Engineering stress and strain
    df['Engineering Stress (MPa)'] = df['Force (N)'] / A_0
    df['Engineering Strain'] = df['Elongation (mm)'] / L_0

    # True stress and strain
    df['True Strain'] = np.log(1 + df['Engineering Strain']) # np.log is the natural logarithm function
    
    df['True Stress (MPa)'] = df['Engineering Stress (MPa)'] * (1 + df['Engineering Strain'])
    
    # Return dataframe with relevant columns only
    df = df[['Engineering Strain', 'Engineering Stress (MPa)', 
            'True Strain', 'True Stress (MPa)']]

    return df