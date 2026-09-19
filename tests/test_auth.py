from sample_app.auth import hash_password, verify_password

def test_password_round_trip():
    salt = b"synthetic-salt"
    hashed = hash_password("correct-password", salt)
    assert verify_password("correct-password", salt, hashed)

def test_wrong_password_fails():
    salt = b"synthetic-salt"
    hashed = hash_password("correct-password", salt)
    assert not verify_password("wrong-password", salt, hashed)
