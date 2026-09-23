def get_allowed_access_levels(user_role: str) -> list[str]:
    """Determine which document access levels a role can retrieve."""
    if user_role == 'student':
        return ['shared', 'student']
    elif user_role == 'teacher':
        return ['shared', 'student', 'teacher']
    return []

def is_access_allowed(user_role: str, document_access_level: str) -> bool:
    return document_access_level in get_allowed_access_levels(user_role)
