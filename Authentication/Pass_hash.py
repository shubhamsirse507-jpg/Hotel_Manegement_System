import hashlib
import os
import binascii


ITERATIONS = 100_000


def hash_password(plain_password: str) -> str:
    """
    Generates a random salt, hashes the password, and returns
    a single string "salt$hash" to store in the DB's
    password_hash column.
    """
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt,
        ITERATIONS
    )
    salt_hex = binascii.hexlify(salt).decode()
    hash_hex = binascii.hexlify(dk).decode()
    return f"{salt_hex}${hash_hex}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """
    Re-hashes plain_password using the stored salt and
    compares it to the stored hash. Returns True/False.
    """
    try:
        salt_hex, hash_hex = stored_hash.split("$")
    except (ValueError, AttributeError):
        return False

    salt = binascii.unhexlify(salt_hex)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt,
        ITERATIONS
    )
    return binascii.hexlify(dk).decode() == hash_hex


if __name__ == "__main__":
    # quick manual test: python password_hash.py
    test_pw = "MySecret123"
    hashed = hash_password(test_pw)
    print("hashed:", hashed)
    print("verify correct pw:", verify_password(test_pw, hashed))
    print("verify wrong pw:", verify_password("wrongpass", hashed))
