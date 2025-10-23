import pandas as pd
from scripts.simulate_data import simulate_stress_strain
from scripts.extract_properties import extract_properties
from scripts.input_validation import validate_inputs

# Step 1: Load user input values from Excel
input_file = "Tensile_Analyzer_MasterWorkbook.xlsx"
material = pd.read_excel(input_file, sheet_name="Dashboard", usecols="B", nrows=1).iloc[0, 0]
override_A_0 = pd.read_excel(input_file, sheet_name="Dashboard", usecols="B", skiprows=2, nrows=1).iloc[0, 0]
override_L_0 = pd.read_excel(input_file, sheet_name="Dashboard", usecols="B", skiprows=3, nrows=1).iloc[0, 0]
use_simulation = pd.read_excel(input_file, sheet_name="Dashboard", usecols="B", skiprows=4, nrows=1).iloc[0, 0]

# Step 2: Load parameter tables
geometry_df = pd.read_excel(input_file, sheet_name="Geometry_Lookup")
properties_df = pd.read_excel(input_file, sheet_name="Material_Properties")

# Step 3: Fetch material parameters
from scripts.material_selector import get_material_properties
material_data = get_material_properties(material, geometry_df, properties_df)

A0 = override_A_0 if pd.notnull(override_A0) else material_data["A_0 (mm²)"]
L0 = override_L_0 if pd.notnull(override_L0) else material_data["L_0 (mm)"]

# Step 4: Simulate or load data
if use_simulation:
    df = simulate_stress_strain(
        E=material_data["Elastic Modulus (MPa)"],
        sigma_y=material_data["Yield Strength (MPa)"],
        K=material_data["Strength Coefficient K (MPa)"],
        n=material_data["n (Strain Hardening Exponent)"],
        L_0=L0,
        A_0=A0,
        strain_max=0.3,
        num_points=100
    )
else:
    df = calculate_stress_strain(
        pd.read_excel(input_file, sheet_name="Input_Data"),
        A_0=A0,
        L_0=L0
    )

# Step 5: Validate and process
validate_inputs(A0, L0, df)

# Step 6: Extract properties
summary = extract_properties(df, material_name=material)
summary_df = pd.DataFrame([summary])

# Step 7: Write outputs to Excel
with pd.ExcelWriter(input_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name="Simulated_Data" if use_simulation else "Imported_Data", index=False)
    summary_df.to_excel(writer, sheet_name="Extracted_Properties", index=False)