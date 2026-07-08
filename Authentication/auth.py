from db import get_connection
from Pass_hash import verify_password
import session


def authenticate(username: str, password: str):
    """
    Checks username/password against the `users` table.
    Returns a user dict on success, or None on failure.
    Also updates last_login and starts the session on success.
    """
    if not username or not password:
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT user_id, staff_id, username, password_hash, role "
            "FROM users WHERE username=%s",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return None

        if not verify_password(password, user["password_hash"]):
            cursor.close()
            conn.close()
            return None

        # success - update last_login
        cursor.execute(
            "UPDATE users SET last_login=NOW() WHERE user_id=%s",
            (user["user_id"],)
        )
        conn.commit()
        cursor.close()
        conn.close()

        # don't keep the password hash around in memory/session
        user.pop("password_hash", None)

        session.start_session(user)
        return user

    except Exception as e:
        print("Authentication error:", e)
        return None


def register_user(staff_id: int, username: str, plain_password: str, role: str):
    """
    Creates a new login for a staff member. role must be one of
    'Admin', 'Receptionist', 'Manager' to match the users table ENUM.
    """
    from Pass_hash import hash_password

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Username already exists."

        hashed = hash_password(plain_password)
        cursor.execute(
            "INSERT INTO users (staff_id, username, password_hash, role) "
            "VALUES (%s,%s,%s,%s)",
            (staff_id, username, hashed, role)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "User registered successfully."

    except Exception as e:
        return False, str(e)


def logout():
    session.end_session()