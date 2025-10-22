import pandas as pd

def calculate_engineering_stress_strain(df, A_0, L_0):
    ''' 
    This function calculates the engineering stress and engineering strain
    of a material based on the input tensile test data
    
    Parameters:
        df (pd.Dataframe): DataFrame with Force (N) and Elongation (mm)
        L_0 (float): Gauge length in mm
        A_0 (float): Cross-sectional area in mm²
    
    Returns:
        pd.Dataframe: DataFrame with Engineering Stress (MPa) and Engineering Strain(unitless).
    
    '''
    df = df.copy()
    df['Engineering Stress (MPa)'] = df['Force (N)'] / A_0
    df['Engineering Strain'] = df['Elongation (mm)'] / L_0
    return df