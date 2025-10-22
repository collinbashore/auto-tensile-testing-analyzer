import numpy as np
import pandas as pd

def simulate_stress_strain(E, sigma_y, K, n, L_0, A_0, num_points=100):
    '''
    Simulates a stress-strain curve using Hooke's Law + Hollomon models.

    Parameters:
        E (float): Elastic modulus in MPa
        sigma_y (float): Yield stress in MPa
        K (float): Strength coefficient in MPa
        n (float): Strain hardening exponent (unitless)
        L_0 (float): Gauge length in mm
        A_0 (float): Cross-sectional area in mm²
        num_points (int): Number of data points to simulate

    Returns:
        pd.DataFrame: DataFrame with Strain, Stress (MPa), Elongation (mm), and Force (N)

    '''
    strain = np.linspace(0, 0.3, num_points)
    
    # Apply linear elastic region until yield point
    if strain < sigma_y / E:
        stress = E * strain  # Hooke’s Law: σ = Eε
    else:
    # Plastic region using Hollomon equation
        stress = K * (strain ** n)
    
    elongation = strain * L_0
    force = (stress * 1e6) * (A_0 * 1e-6) # 1 MPa = 10^6 Pa and 1 mm² = 10^(-6) m²
    return pd.DataFrame({
        "Strain": strain,
        "Stress (MPa)": stress,
        "Elongation (mm)": elongation,
        "Force (N)": force
    })