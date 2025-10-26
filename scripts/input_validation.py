import pandas as pd


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
    # Check that required scalar inputs are positive
    if A_0 <= 0 or L_0 <= 0:
        raise ValueError(
            "Cross-sectional area and gauge length must be greater "
            "than zero."
        )

    # Fail if any cell in the DataFrame is missing
    if df.isnull().values.any():
        raise ValueError("Data contains null values.")

    # Verify required columns exist in the DataFrame
    if 'Force (N)' not in df.columns or 'Elongation (mm)' not in df.columns:
        raise ValueError("Missing required columns in data.")

    # All validations passed
    return True


def validate_override(value, default, name):
    """
    Validates an override value for A_0 or L_0.

    Parameters:
    -----------
    value : any
        The override value to validate. Can be None if no override is provided.

    default : float
        The default value to use if no override is provided.

    name : str
        The name of the parameter being validated (for logging/debugging
        purposes).

    Raises:
    -------
    ValueError:
        - If the override value is provided but is not a positive number.

    Returns:
    --------
    float
        The validated override value (or default if None is provided).
    """
    try:
        # If cell is blank (NaN, None, or empty string), use default value
        if pd.isna(value) or value == "":
            print(f"{name} override not provided. Using default: {default}")
            return default

        # Convert to float if valid
        return float(value)

    except ValueError:
        # If conversion fails or value is invalid, raise error
        print(f"Invalid {name} override value provided: {value}. "
              f"Using default: {default}")
    return default
