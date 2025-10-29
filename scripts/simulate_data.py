import numpy as np
import pandas as pd


def simulate_stress_strain(
        E, sigma_y, K, n, L_0, A_0, uts, strain_max=0.3, num_points=100, decay_factor=15):
    """
    This function generates synthetic tensile test data that includes:
    - Engineering stress-strain values
    - True stress-strain values
    - Elongation and Force

    Hooke's Law (σ = E·ε) models the linear elastic region; the plastic
    region uses an expanded Hollomon's Law:
    σ = σ_y + K·(ε - ε_y)^n.

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
    # Generate engineering strain from 0 to strain_max
    eng_strain = np.linspace(0, strain_max, num_points)

    # Yield strain ε_y from σ_y (MPa) and E (GPa -> MPa)
    yield_strain = sigma_y / (E * 1e3)

    # Ultimate tensile strain from UTS (MPa) and E (GPa -> MPa)
    uts_strain = uts / (E * 1e3)

    # Engineering stress (MPa)
    # - Elastic: compute in MPa
    elastic_mpa = (E * 1e3) * eng_strain

    # - Plastic: compute in MPa
    plastic_mpa = sigma_y + K * (
        np.maximum(eng_strain - yield_strain, 0.0)
    ) ** n

    # Compute Engineering Stress (MPa) using piecewise function
    # np.piecewise(array of values, conditions (in a list), functions (in a list))
    eng_stress = np.piecewise(eng_strain,
        [eng_strain < yield_strain, (yield_strain >= eng_strain) & (eng_strain <= uts_strain), eng_strain > uts_strain],
        [elastic_mpa, plastic_mpa,
         plastic_mpa * np.exp(-decay_factor * (eng_strain - uts_strain))]
    )

    # Kinematics and force
    elongation = eng_strain * L_0  # mm

    # force = stress(MPa)* A0 (mm²) = N
    # 1 MPa = 1 N/mm²
    force = eng_stress * A_0

    # True measures
    true_strain = np.log1p(eng_strain)  # log(1+ε)
    true_stress = eng_stress * (1 + eng_strain)

    # Assemble DataFrame
    return pd.DataFrame({
        "Force (N)": force,
        "Elongation (mm)": elongation,
        "Engineering Strain": eng_strain,
        "Engineering Stress (GPa)": eng_stress,
        "True Strain": true_strain,
        "True Stress (GPa)": true_stress,
    })
