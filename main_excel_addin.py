
from scripts.user_inputs import get_user_inputs
from scripts.input_validation import validate_inputs
from scripts.materials_selector import get_material_properties
from scripts.simulate_data import simulate_stress_strain
from scripts.calculate_stress_strain import calculate_stress_strain
from scripts.extract_properties import extract_properties
from scripts.visualize import plot_engineering_true_combined_subplots
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import pandas as pd
from pathlib import Path

def run_main():
    # Define file path
    workbook_path = Path("Tensile_Analyzer_MasterWorkbook.xlsx")

    # Step 1: Get user inputs from Dashboard sheet
    material, override_A0, override_L0, use_simulation = get_user_inputs(workbook_path)

    # Step 2: Validate inputs
    validate_inputs(material, override_A0, override_L0, use_simulation)

    # Step 3: Get material properties and geometry
    material_props = get_material_properties(material, override_A0, override_L0)

    # Step 4: Simulate or Calculate data
    if use_simulation:
        df = simulate_stress_strain(material_props)
        df.to_excel(workbook_path, sheet_name="Simulated_Data", index=False)
    else:
        input_df = pd.read_excel(workbook_path, sheet_name="Input_Data")
        df = calculate_stress_strain(input_df, material_props)
        df.to_excel(workbook_path, sheet_name="Stress_Strain_Calculations", index=False)

    # Step 5: Extract mechanical properties
    properties = extract_properties(df)
    properties_df = pd.DataFrame([properties])
    properties_df.to_excel(workbook_path, sheet_name="Properties_Extracted", index=False)

    # Step 6: Generate plot
    fig = plot_engineering_true_combined_subplots(df, material)
    fig_path = Path("plot.png")
    fig.savefig(fig_path, dpi=300)

    # Step 7: Insert plot into Dashboard
    wb = load_workbook(workbook_path)
    ws = wb["Dashboard"]
    img = Image(str(fig_path))
    ws.add_image(img, "E10")
    wb.save(workbook_path)

    return f"Dashboard updated for material: {material}"
