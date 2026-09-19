import hashlib
import hmac

def hash_password(password: str, salt: bytes) -> str:
    # Demonstration only. A real application should use a dedicated password KDF
    # such as Argon2id/bcrypt with appropriate parameters.
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return digest.hex()

def verify_password(password: str, salt: bytes, expected_hex: str) -> bool:
    return hmac.compare_digest(hash_password(password, salt), expected_hex)
