import numpy as np
import pandas as pd

def simulate_stress_strain(E, sigma_y, K, n, L_0, A_0, strain_max=0.3, num_points=100):
    """
    This function generates synthetic tensile test data that includes:
    - Engineering stress-strain values
    - True stress-strain values
    - Elongation and Force

    Hooke's Law (σ = E * ε) is used to model the linear elastic region, while the plastic 
    region is modeled using the expanded Hollomon's Law (σ = σ_y + K * (ε - ε_y)^n).

    Parameters:
    -----------
    E (float): 
        Elastic modulus in GPa.
    sigma_y (float): 
        Yield stress (strength) in MPa.
    K (float): 
        Strength coefficient in MPa.
    n (float): 
        Strain hardening exponent (unitless).
    L_0 (float): 
        Gauge length in mm.
    A_0 (float): 
        Cross-sectional area in mm².
    strain_max (float, optional): 
        Maximum engineering strain to simulate. Default is 0.3 (30%).
    num_points (int, optional): 
        Number of data points to simulate. Default is 100.

    Returns:
    --------
    pd.DataFrame:
        A DataFrame containing the following columns:
        - "Force (N)"
        - "Elongation (mm)"
        - "Engineering Strain"
        - "Engineering Stress (GPa)"
        - "True Strain"
        - "True Stress (GPa)"
    """
    # Generates a numpy array of strain (engineering) values from 
    # 0 to strain_max based on num_points
    eng_strain = np.linspace(0, strain_max, num_points)  
    
    # Calculate yield strain (ε_y) from yield strength (σ_y) and elastic modulus (E)
    yield_strain = sigma_y / E 
    
    # Calculate values of stress (engineering) in the eng_stress array based on the values 
    # in the eng_strain array:
    eng_stress = np.where(
        eng_strain <= yield_strain, # Condition: If engineering strain (ε) is below or 
                                    # equal to the yield strain (elastic region)
        
        E * eng_strain, # Hooke's Law (σ = E * ε) if engineering strain (ε) is below or 
                        # equal to the yield strain (elastic region)

        (sigma_y * 1e-3) + K * (eng_strain - yield_strain) ** n # Expanded version of Hollomon's Law 
        # (σ = σ_y + K * (ε - e_y)^n) if engineering strain (ε) is beyond the yield point (plastic region)
    )
    
    # The code above calculates values for engineering stress above by applying the np.where function 
    # (in a compact, vectorized way) conditionally:
    
    # np.where(condition, value_if_true, value_if_false)
    
    # Think of the np.where function as this: "if this condition is true, use this value; otherwise, use that value" for each element in the eng_strain array.
    
    elongation = eng_strain * L_0 # Elongation in mm
    force = (eng_stress * 1e3) * A_0 # 1 GPa = 10^3 MPa and 1 MPa = 1 N/mm² needed to convert to Newtons.
    
    # Calculate true stress and true strain
    true_strain = np.log(1 + eng_strain) # np.log is the natural logarithm function
    true_stress = eng_stress * (1 + eng_strain)
    
    # Return as DataFrame
    return pd.DataFrame({
        "Force (N)": force,
        "Elongation (mm)": elongation,
        "Engineering Strain": eng_strain,
        "Engineering Stress (GPa)": eng_stress,
        "True Strain": true_strain,
        "True Stress (GPa)": true_stress
    })  