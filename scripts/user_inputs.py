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
    dashboard = pd.read_excel(file_path, sheet_name="Dashboard", usecols="B", nrows=6)

    # Step 2: Extract individual values
    material = dashboard.iloc[0, 0] # Material name from cell B1
    override_A0 = dashboard.iloc[2, 0] # Override A0 from cell B3
    override_L0 = dashboard.iloc[3, 0] # Override L0 from cell B4
    use_simulation = dashboard.iloc[4, 0] # Use simulate data (TRUE) or real data (FALSE) from cell B5

    # Step 3: Begin validations

    # Material name must not be empty or NaN
    if pd.isna(material) or not isinstance(material, str) or material.strip() == "":
        raise ValueError("Material name is missing or invalid. Please select a material in cell B1.")

    # A0 and L0 are optional, but if they are provided, they must be positive numbers
    if pd.notna(override_A0):
        if not isinstance(override_A0, (int, float)) or override_A0 <= 0:
            raise ValueError("Override A₀ must be a positive number.")

    if pd.notna(override_L0):
        if not isinstance(override_L0, (int, float)) or override_L0 <= 0:
            raise ValueError("Override L₀ must be a positive number.")

    # use_simulation must be a boolean (TRUE or FALSE in Excel)
    if not isinstance(use_simulation, bool):
        raise ValueError("Use Simulation must be either TRUE or FALSE in cell B5.")

    return material, override_A0, override_L0, use_simulation