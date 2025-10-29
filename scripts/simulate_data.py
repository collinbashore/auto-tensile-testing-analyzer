import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def simulate_stress_strain(
        E, sigma_y, K, n, L_0, A_0, strain_max=0.3, num_points=100, fit_decay=True, default_decay=15):
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
        - "Engineering Stress (MPa)"
        - "True Strain"
        - "True Stress (MPa)"
    """
    # Generate engineering strain from 0 to strain_max
    eng_strain = np.linspace(0, strain_max, num_points)

    # Yield strain ε_y from σ_y (MPa) and E (GPa -> MPa)
    yield_strain = sigma_y / (E * 1e3)

    # Ultimate tensile strain from UTS (MPa) and E (GPa -> MPa)
    # uts_strain = uts / (E * 1e3)  # This will be calculated by fit_decay_factor

    # Engineering stress (MPa)
    # - Elastic: compute in MPa
    elastic_mpa = (E * 1e3) * eng_strain

    # - Plastic: compute in MPa
    plastic_mpa = sigma_y + K * (
        np.maximum(eng_strain - yield_strain, 0.0)
    ) ** n

    def exponential_decay(eng_strain, decay_factor, uts, uts_strain):
        """Exponential decay function for post-UTS region.

        Parameters:
        -----------
        eng_strain : np.ndarray
            The engineering strain values.
        decay_factor : float
            The decay factor for the exponential function.
        uts : float
            The ultimate tensile strength.
        uts_strain : float
            The strain at ultimate tensile strength.

        Returns:
        --------
        np.ndarray
            The computed stress values after UTS.
        """
        return uts * np.exp(-decay_factor * (eng_strain - uts_strain))


    def fit_decay_factor(eng_strain, eng_stress):
        """Fit decay factor based on stress at a strain beyond UTS.

        Parameters:
        -----------
        eng_strain : np.ndarray
            The engineering strain values.
        eng_stress : np.ndarray
            The corresponding stress values.

        Returns:
        --------
        float
            The fitted decay factor.
        """
        uts_index = np.argmax(eng_stress)
        uts_strain = eng_strain[uts_index]
        uts = eng_stress[uts_index]
        post_strain = eng_strain[uts_index:]
        post_stress = eng_stress[uts_index:]
        default_decay = 15
        try:
            popt, _ = curve_fit(
                lambda eps, d: exponential_decay(eps, d, uts, uts_strain),
                post_strain,
                post_stress,
                p0=[default_decay],
                bounds=(0, 100)
            )
            return popt[0], uts, uts_strain
        except RuntimeError:
            return default_decay, uts, uts_strain



    # Compute Engineering Stress (MPa) using piecewise function
    # np.piecewise(array of values, conditions (in a list), functions (in a list))
    eng_stress = np.where(eng_strain <= yield_strain,
                        elastic_mpa,
                        plastic_mpa
    )

    if fit_decay:
        decay_factor, uts, uts_strain = fit_decay_factor(eng_strain, eng_stress)
        post_uts_mask = eng_strain > uts_strain
        eng_stress[post_uts_mask] = exponential_decay(eng_stress[post_uts_mask], decay_factor, uts, uts_strain)

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
