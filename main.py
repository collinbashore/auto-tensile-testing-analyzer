# Import all necessary Python libraries and objects
import pandas as pd # For data manipulation
import matplotlib.pyplot as plt # For data visualization
from pathlib import Path # For handling file paths
from openpyxl import load_workbook # For Excel file operations
from openpyxl.drawing.image import Image # For handling images in Excel

# Import all modules from the 'scripts' file directory
from scripts.materials_selector import get_material_properties
from scripts.input_validation import validate_inputs
from scripts.user_inputs import get_user_inputs
from scripts.simulate_data import simulate_stress_strain
from scripts.calculate_stress_strain import calculate_stress_strain
from scripts.extract_properties import extract_properties
from scripts.visualize import plot_engineering_true_combined_subplots

# Step 1: Create a Path object pointing to an Excel file
file_path = Path("Tensile_Analyzer_MasterWorkbook.xlsx")

# Step 2: Get user inputs from Dashboard sheet
material_name, override_A0, override_L0, use_simulation = get_user_inputs(file_path)

# Step 3: Get material properties and validate geometry
geometry_df = pd.read_excel(file_path, sheet_name="Geometry_Lookup")
properties_df = pd.read_excel(file_path, sheet_name="Material_Properties")

material_props = get_material_properties(material_name, geometry_df, properties_df)

# Override A_0 and L_0 from Dashboard if given
# prefer dashboard overrides; fall back to material properties
A_0 = override_A0 if override_A0 is not None else material_props["A_0 (mm²)"]
L_0 = override_L0 if override_L0 is not None else material_props["L_0 (mm)"]

# store final geometry back into material_props for consistency
material_props["A_0 (mm²)"] = A_0
material_props["L_0 (mm)"] = L_0

# Step 4: Generate stress-strain data
if use_simulation:
    # Simulate stress-strain data using material properties
    df = simulate_stress_strain(
        E=material_props["Elastic Modulus (MPa)"],
        sigma_y=material_props["Yield Strength (MPa)"],
        K=material_props["Strength Coefficient K (MPa)"],
        n=material_props["n (Strain Hardening Exponent)"],
        L_0=L_0,
        A_0=A_0,
    )
    output_sheet_name = "Simulated_Data"
else:
    # Use raw data from Input_Data sheet
    df_raw = pd.read_excel(file_path, sheet_name="Input_Data")
    validate_inputs(A_0, L_0, df_raw)
    df = calculate_stress_strain(df_raw, A_0=A_0, L_0=L_0)
    output_sheet_name = "Stress_Strain_Calculations"

# Step 5: Extract properties
summary = extract_properties(df, material_props)
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name=output_sheet_name, index=False)
    summary_df = pd.DataFrame([summary])
    summary_df.to_excel(writer, sheet_name="Extracted_Properties", index=False)

# Step 6: Generate visualizations

# This comes after loading/processing the dataframe (df) and material_name
fig = plot_engineering_true_combined_subplots(df, material_name)

# Save the figure to a image file
plot_path = Path("stress_strain_plots.png")
fig.savefig(plot_path, dpi=300) # dpi=300 for high resolution

# Load the Excel workbook and select the 'Dashboard' sheet
workbook_path = Path("Tensile_Analyzer_MasterWorkbook.xlsx")
wb = load_workbook(workbook_path)
ws = wb["Dashboard"]

# Insert the image into a specific cell (e.g., H10)
img = Image(str(plot_path))
ws.add_image(img, "H10")

# Save the workbook with the plots inserted
wb.save(workbook_path)