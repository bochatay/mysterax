def select_version(versions_dict, current_bools, current_inventory, current_inputs):
    """
    Sélectionne une version selon les conditions :
    - priorité aux versions dont TOUTES les conditions sont remplies
    - sinon version sans condition
    - sinon (None, False)
    """

    default_key = None
    default_version = None

    print(current_bools)
    print(current_inputs)
    for version_key, version in versions_dict.items():
        conditions = version.get("condition", {})
        print("version room" , version_key)
        print(conditions)

        # --- Version par défaut (sans condition) ---
        if not conditions:
            default_key = version_key
            default_version = version
            continue

        # --- Conditions booléennes ---
        bool_conditions = conditions.get("requires_bools", {})
        bools_ok = all(
            current_bools.get(bool_id) == required_state
            for bool_id, required_state in bool_conditions.items()
        )

        # --- Conditions objets ---
        required_objects = conditions.get("requires_objects", {})
        objects_ok = all(
            (obj in current_inventory) == required_state
            for obj, required_state in required_objects.items()
        )
        '''
        required_objects = conditions.get("requires_objects", [])
        objects_ok = all(
            obj in current_inventory
            for obj in required_objects
        )
        '''

        # --- Conditions input ---
        required_inputs = conditions.get("requires_inputs", {})
        inputs_ok = all(
            current_inputs.get(input_id) == required_state
            for input_id, required_state in required_inputs.items()
        )
        
        print(bools_ok,objects_ok,inputs_ok)

        # --- Toutes les conditions doivent être vraies ---
        if bools_ok and objects_ok and inputs_ok:
            return version_key, version

    # Aucune version conditionnelle valide → version par défaut
    if default_version is not None:
        return default_key, default_version

    # Aucune version possible
    return None, False
