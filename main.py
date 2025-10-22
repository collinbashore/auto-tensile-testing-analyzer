# --- Imported Libraries and Files ---
import pandas as pd
from scripts.material_selector import get_material_properties
from scripts.simulate_data import simulate_stress_strain
from scripts.calculate_stress_strain import calculate_engineering_stress_strain
from scripts.extract_properties import extract_properties
from scripts.visualize import plot_stress_strain
from scripts.input_validation import validate_inputs

# --- Load lookup tables ---
geometry_df = pd.read_excel("Tensile_Analyzer_MasterWorkbook.xlsx", sheet_name="Geometry_Lookup")
properties_df = pd.read_excel("Tensile_Analyzer_MasterWorkbook.xlsx", sheet_name="Material_Properties")

# --- Simulation or Real Data ---
if use_simulation:
    df = simulate_stress_strain(
        E=material_data["Elastic Modulus (MPa)"],
        sigma_y=material_data["Yield Strength (MPa)"],
        K=material_data["Strength Coefficient K (MPa)"],
        n=material_data["n (Strain Hardening Exponent)"],
        L_0=L_0,
        A_0=A_0
    )
    df = calculate_engineering_stress_strain(df, A_0, L_0)
else:
    df = pd.read_excel("Tensile_Analyzer_MasterWorkbook.xlsx", sheet_name="Input_Data")
    validate_inputs(A_0, L_0, df)
    df = calculate_engineering_stress_strain(df, A_0, L_0)

# --- Extract Materials Properties ---
properties = extract_properties(df)

# --- Output Results ---
print(f"Material: {selected_material}")
print("Extracted Mechanical Properties:")
for key, value in properties.items():
    print(f"{key}: {value:.2f}")

# --- Plot Curve ---
plot_stress_strain(df)