def validate_inputs(A_0, L_0, df):
    """
    This function validates the inputs required for stress-strain calculations.

    Parameters:
    -----------
    A_0 : float
        Initial cross-sectional area of the specimen in mm².
        Must be greater than zero.

    L_0 : float
        Initial gauge length of the specimen in mm.
        Must be greater than zero.

    df : pd.DataFrame
        Input data table (real or simulated) that must include:
            - 'Force (N)': Applied force values in Newtons
            - 'Elongation (mm)': Elongation measurements in mm

    Raises:
    -------
    ValueError:
        - If A_0 or L_0 is less than or equal to zero
        - If the DataFrame contains any null (missing) values
        - If required columns ('Force (N)', 'Elongation (mm)') are missing

    Returns:
    --------
    True
        Returns True if all inputs are valid.

    Purpose:
    --------
    Ensures that input data is valid before proceeding with
    mechanical property calculations. Prevents runtime errors
    and ensures data quality and integrity.
    """
    if A_0 <= 0 or L_0 <= 0:
        raise ValueError("Cross-sectional area and gauge length must be greater than zero.")
    if df.isnull().values.any():
        raise ValueError("Data contains null values.")
    if 'Force (N)' not in df.columns or 'Elongation (mm)' not in df.columns:
        raise ValueError("Missing required columns in data.")
    return True