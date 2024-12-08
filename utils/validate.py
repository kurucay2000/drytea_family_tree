def validate_parent(parent_name, family_tree):
    """
    Validates if a parent exists in the family tree.

    Args:
        parent_name (str): Name of the parent to validate
        family_tree: The family tree instance

    Returns:
        bool: True if parent exists or if parent_name is empty
    """
    if not parent_name:  # Empty parent field is valid
        return True

    # Check if parent exists in members list
    return any(
        member.get("name", "").lower() == parent_name.lower()
        for member in family_tree.members.values()
    )
