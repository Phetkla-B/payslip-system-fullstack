from app.core.security import hash_password, verify_password

def test_password_hash():
    pw = "1234"
    hashed = hash_password(pw)

    assert verify_password(pw, hashed) == True
    assert verify_password("wrong", hashed) == False