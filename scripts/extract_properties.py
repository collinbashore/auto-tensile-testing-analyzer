def extract_properties(df, material_name='Unknown'):
    ''' 
    This function extracts key mechanical properties from the stress-strain DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        A DataFrame containing engineering stress-strain data.
        Must include the following columns:
            - 'Engineering Strain'
            - 'Engineering Stress (MPa)'

    material_name : str, optional
        Name of the material. Default is 'Unknown'.
        This will appear as the first column in the output.

    Returns:
    --------
    pd.DataFrame
        A single-row DataFrame with the following columns:
            - 'Material': Name of the material
            - 'Elastic Modulus': Approximated from first two points
            - 'Yield Strength': First stress value after strain > 0.002 (0.2% offset method)
            - 'UTS': Ultimate tensile strength (maximum stress)
            - 'Fracture Strain': Last strain value in the dataset (i.e., failure point)
    
    Notes:
    ------
    This function assumes that the input data is sorted by increasing strain.
    It uses simple methods for estimating properties and is ideal for simulation 
    or educational purposes.
    
    ''' 
    elastic_modulus = df['Engineering Stress (MPa)'].iloc[1] / df['Engineering Strain'].iloc[1]
    yield_strength = df[df['Engineering Strain'] > 0.002]['Engineering Stress (MPa)'].iloc[0]
    uts = df['Engineering Stress (MPa)'].max()
    fracture_strain = df['Engineering Strain'].iloc[-1]
    return {
        "Material": material_name,
        "Elastic Modulus": elastic_modulus,
        "Yield Strength": yield_strength,
        "UTS": uts,
        "Fracture Strain": fracture_strain
    }