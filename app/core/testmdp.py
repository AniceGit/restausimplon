from security import get_password_hash, verify_password
def test_verify_password():
    password = "testpassword"
    print("Testing password hashing and verification...")
    hashed_password = get_password_hash(password)
    print(f"Hashed password: {hashed_password}")
    assert verify_password(password, hashed_password) == True
    print("Password verification successful.")
    assert verify_password("wrongpassword", hashed_password) == False
    print("Wrong password verification failed as expected.")

test_verify_password()