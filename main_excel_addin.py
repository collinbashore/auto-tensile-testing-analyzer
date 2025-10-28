# Main Excel Add-in Script for Tensile Test Analyzer


def run_main():
    '''Main function to run the tensile test analyzer Excel add-in workflow.

    Returns:
        df (pd.DataFrame): DataFrame containing stress-strain data.
        properties (dict): Extracted mechanical properties.
        fig (matplotlib.figure.Figure): Generated plot figure.
    '''

    # Import necessary modules and libraries
    from scripts.user_inputs import get_user_inputs
    from scripts.input_validation import validate_inputs
    from scripts.materials_selector import get_material_properties
    from scripts.simulate_data import simulate_stress_strain
    from scripts.calculate_stress_strain import calculate_stress_strain
    from scripts.extract_properties import extract_properties
    from scripts.visualize import plot_engineering_true_combined_subplots
    import pandas as pd
    from pathlib import Path

    # Define file path
    workbook_path = Path("Tensile_Analyzer_MasterWorkbook.xlsx")

    # Step 1: Get user inputs from Dashboard sheet
    material, A_0, L_0, use_simulation = get_user_inputs(workbook_path)

    # Step 2: Validate inputs
    validate_inputs(material, A_0, L_0, use_simulation)

    # Step 3: Get material properties and geometry
    geometry_df = pd.read_excel(
        workbook_path,
        sheet_name="Geometry_Lookup"
    )
    properties_df = pd.read_excel(
        workbook_path,
        sheet_name="Material_Properties"
    )
    material_props = get_material_properties(
        material, geometry_df, properties_df
    )

    # Step 4: Update A_0 and L_0 with user overrides if provided
    A0_final = A_0 if A_0 is not None else material_props['A_0 (mm²)']
    L0_final = L_0 if L_0 is not None else material_props['L_0 (mm)']
    material_props['A_0 (mm²)'] = A0_final
    material_props['L_0 (mm)'] = L0_final

    # Step 4: Simulate or Calculate data
    # If the user clicked the checkbox to use simulated data
    if use_simulation:
        df = simulate_stress_strain(
            E=material_props['Elastic Modulus (GPa)'],
            sigma_y=material_props['Yield Strength (MPa)'],
            K=material_props['Strength Coefficient K (MPa)'],
            n=material_props['n (Strain Hardening Exponent)'],
            A_0=A0_final,
            L_0=L0_final
        )
        df.to_excel(workbook_path, sheet_name="Simulated_Data",
                    index=False)
    else:
        input_df = pd.read_excel(workbook_path, sheet_name="Input_Data")
        validate_inputs(A0_final, L0_final, input_df)
        df = calculate_stress_strain(input_df, A_0=A0_final, L_0=L0_final)
        df.to_excel(workbook_path,
                    sheet_name="Stress_Strain_Calculations",
                    index=False)

    # Step 5: Extract mechanical properties
    properties_df = extract_properties(df)  # Now returns DataFrame directly
    properties_df.to_excel(workbook_path,
                           sheet_name="Properties_Extracted",
                           index=False)

    # Step 6: Generate plot
    fig = plot_engineering_true_combined_subplots(df, material)
    fig_path = Path("plot.png")
    fig.savefig(fig_path, dpi=300)

    # Step 7: Insert plot into Dashboard
    from openpyxl import load_workbook
    from openpyxl.drawing.image import Image

    wb = load_workbook(workbook_path)
    ws = wb["Dashboard"]
    img = Image(str(fig_path))
    ws.add_image(img, "B13")
    wb.save(workbook_path)

    return df, properties_df, fig
