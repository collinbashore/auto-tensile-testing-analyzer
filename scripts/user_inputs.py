import pandas as pd

def get_user_inputs(file_path):
    """
    Reads user input values from the 'Dashboard' sheet of the Excel file and validates them.

    Parameters:
    -----------
    file_path : str
        Path to the Excel file.

    Returns:
    --------
    tuple
        A tuple containing:
        - material (str)
        - override_A0 (float or None)
        - override_L0 (float or None)
        - use_simulation (bool)

    Raises:
    -------
    ValueError
        If required values are missing or of the wrong type.
    """

    # Step 1: Read the first 6 rows of only column B from the Dashboard sheet
    dashboard = pd.read_excel(file_path, sheet_name="Dashboard", usecols="C", nrows=12)

    # Step 2: Extract individual values
    material = dashboard.iloc[4, 0] # Material name from cell C5
    override_A0 = dashboard.iloc[8, 0] # Override A0 from cell C9
    override_L0 = dashboard.iloc[9, 0] # Override L0 from cell C10
    use_simulation = dashboard.iloc[5, 0] # Use simulate data (TRUE) or real data (FALSE) from cell C6

    # Step 3: Begin validations

    # Material name must not be empty or NaN
    if pd.isna(material) or not isinstance(material, str) or material.strip() == "":
        raise ValueError("Material name is missing or invalid. Please select a material in cell C5.")

    # A0 and L0 are optional, but if they are provided, they must be positive numbers
    if pd.notna(override_A0) and (not isinstance(override_A0, (int, float)) or override_A0 <= 0):
        raise ValueError("Override A_0 must be a positive number.")

    if pd.notna(override_L0) and (not isinstance(override_L0, (int, float)) or override_L0 <= 0):
        raise ValueError("Override L_0 must be a positive number.")

    # use_simulation must be a boolean (TRUE or FALSE in Excel)
    if not isinstance(use_simulation, bool):
        raise ValueError("Use Simulation must be either TRUE or FALSE in cell C6.")

    return material, override_A0, override_L0, use_simulation