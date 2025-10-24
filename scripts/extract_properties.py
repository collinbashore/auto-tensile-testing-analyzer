import numpy as np

def extract_properties(df, material_name='Unknown'):
    ''' 
    This function extracts key mechanical properties from the stress-strain DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        A DataFrame containing engineering stress-strain data.
        Must include the following columns:
            - 'Engineering Strain'
            - 'Engineering Stress (GPa)'
            - 'True Strain'
            - 'True Stress (GPa)'

    material_name : str, optional
        Name of the material. Default is 'Unknown'.
        This will appear as the first column in the output.

    Returns:
    --------
    pd.DataFrame
        A single-row DataFrame with the following columns:
            - 'Material': Name of the material
            - 'Elastic Modulus (GPa)': Approximated from first two points
            - 'Yield Strength (MPa)': First stress value after strain > 0.002 (0.2% offset method)
            - 'Ultimate Tensile Strength (UTS, MPa)': Ultimate tensile strength (maximum stress)
            - 'Fracture Strain': Last strain value in the dataset (i.e., failure point)
            - 'Percent Elongation (%)': Fracture strain expressed as a percentage
            - 'Toughness (MPa or MJ/m^3)': Area under the full engineering stress-strain curve (up to fracture)
            - 'Resilience (MPa or MJ/m^3)': Area under the stress-strain curve up to yield point
            - 'True Stress at UTS (GPa)': True stress corresponding to UTS
            - 'Necking strain': True strain at UTS
            - 'Percent Reduction in Area (%)': Calculated from true fracture strain (or from the initial and 
            final cross-sectional areas if available)
    
    Notes:
    ------
    This function assumes that the input data is sorted by increasing strain.
    It uses simple methods for estimating properties and is ideal for simulation or educational purposes.
    
    ''' 

    # Calculate Elastic Modulus (Young's Modulus) using the first two data points (the first data point is 
    # the origin of the plot (skipped in calculation), only the second data point ()index 1, not 0) is needed)
    # Formula: E = stress / strain (only valid in the elastic region)
    elastic_modulus = df['Engineering Stress (GPa)'].iloc[1] / df['Engineering Strain'].iloc[1]

    # Estimate Yield Strength using 0.2% offset method (approximation)
    # Find the first stress value where strain exceeds 0.002 (0.2%)
    yield_strength = df[df['Engineering Strain'] > 0.002]['Engineering Stress (GPa)'].iloc[0]
    yield_strength *= 1e3  # Convert GPa to MPa for yield strength

    # Find the Ultimate Tensile Strength (UTS), which is the maximum stress value in the dataset
    uts = df['Engineering Stress (GPa)'].max()
    uts *= 1e3  # Convert GPa to MPa for UTS

    # Get the Fracture Strain, which is the last strain value recorded (where the material breaks)
    fracture_strain = df['Engineering Strain'].iloc[-1]
    
    # Calculate percent elongation at fracture
    percent_elongation = fracture_strain * 100  # Convert to percentage
    
    # Toughness = Area under full engineering stress-strain curve
    # np.trapz does numerical integration using the trapezoidal rule
    toughness = np.trapz(df['Engineering Stress (GPa)'], df['Engineering Strain'])
    toughness *= 1e3  # Convert GPa to MPa (MJ/m^3)

    # Resilience = Area under elastic region (linear approx.)
    resilience = (yield_strength ** 2) / (2 * elastic_modulus * 1e3)  # Convert GPa to MPa for modulus

    # True Stress at UTS = Use index of max engineering stress
    uts_index = df['Engineering Stress (GPa)'].idxmax()
    true_stress_at_uts = df['True Stress (GPa)'].iloc[uts_index]

    # Necking strain = True strain at max true stress (usually post-UTS)
    necking_index = df['True Stress (GPa)'].idxmax()
    necking_strain = df['True Strain'].iloc[necking_index]

    # Percent Reduction in Area (%RA)
    # ε_tf = ln(A0 / Af) => %RA = (1 - exp(-ε_tf)) * 100
    true_fracture_strain = df['True Strain'].iloc[-1]
    percent_reduction_area = (1 - np.exp(-true_fracture_strain)) * 100
    
    # Return all calculated properties in a dictionary format, including the material name
    return {
        "Material": material_name,
        "Elastic Modulus (GPa)": elastic_modulus,
        "Yield Strength (MPa)": yield_strength,
        "Ultimate Tensile Strength (UTS, MPa)": uts,
        "Fracture Strain": fracture_strain,
        "Percent Elongation (%)": percent_elongation,
        "Toughness (MPa)": toughness,
        "Resilience (MPa)": resilience,
        "True Stress at UTS (GPa)": true_stress_at_uts,
        "Necking strain": necking_strain,
        "Percent Reduction in Area (%)": percent_reduction_area
    }