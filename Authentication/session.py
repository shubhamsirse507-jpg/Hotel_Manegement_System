# =====================================================
# Session Handling (1.3.4)
# Simple in-memory session for a desktop app - holds the
# currently logged-in user for as long as the app is running.
# =====================================================

_current_user = None


def start_session(user):
    """
    user: dict like {"user_id":.., "username":.., "role":.., "staff_id":..}
    Call this right after a successful login.
    """
    global _current_user
    _current_user = user


def get_current_user():
    """Returns the logged-in user dict, or None if nobody is logged in."""
    return _current_user


def is_logged_in():
    return _current_user is not None


def get_role():
    """Convenience helper - returns the current user's role, or None."""
    return _current_user["role"] if _current_user else None


def end_session():
    """Call this on logout."""
    global _current_user
    _current_user = None