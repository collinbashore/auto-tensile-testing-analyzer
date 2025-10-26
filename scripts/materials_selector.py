

def get_material_properties(material, geometry_df, properties_df):
    """
    Retrieves and combines geometry and mechanical property data for a
    given material.

    Parameters:
    -----------
    material : str
        Name of the material to look up (case-insensitive).
        This should match the 'Material' column in both geometry_df and
        properties_df.

    geometry_df : DataFrame
        A DataFrame containing geometric information for materials.
        Must include a 'Material' column and columns like 'A_0 (mm²)',
        'L_0 (mm)', etc.

    properties_df : DataFrame
        A DataFrame containing mechanical property information for
        materials.
        Must also include a 'Material' column and columns like 'E', 'K',
        'n', 'sigma_y', etc.

    Returns:
    --------
    dict
        A merged dictionary of geometry and mechanical properties for the
        specified material.
        Example keys might include:
            - 'A_0 (mm²)'
            - 'L_0 (mm)'
            - 'Elastic Modulus (MPa)'
            - 'Yield Strength (MPa)'
            - 'Strength Coefficient K (MPa)'
            - 'n (Strain Hardening Exponent)'

    Raises:
    -------
    ValueError
        If the material is not found in either the geometry_df or
        properties_df.

    Notes:
    ------
    - Matching is case-insensitive.
    - Combines rows from both datasets into a single dictionary using
      unpacking (**).
    - Useful for simulations and calculations that require both geometry
      and mechanical inputs.
    """
    # Convert material name to lowercase and find its matching row in the
    # geometry DataFrame
    geo_row = geometry_df[
        geometry_df["Material"].str.lower() == material.lower()
    ]

    # Do the same for the material properties DataFrame
    prop_row = properties_df[
        properties_df["Material"].str.lower() == material.lower()
    ]

    # If either row is not found (i.e., material is missing), raise an
    # error and stop the program
    if geo_row.empty or prop_row.empty:
        raise ValueError(f"Material '{material}' not found.")

    # Convert the single matching row for geometry into a dictionary
    # (key-value format)
    geometry = geo_row.iloc[0].to_dict()

    # Do the same for the properties row
    properties = prop_row.iloc[0].to_dict()

    # Merge the two dictionaries (geometry + properties) and return the
    # combined result
    # This allows access to all material parameters (dimensions +
    # properties) in one place
    return {**geometry, **properties}
