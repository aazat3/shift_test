from shift_test.src.core.security import (
    password_hash,
    verify_password,
    create_access_token,
)


def test_password_hash():

    password = "secret123"
    hashed = password_hash(password)
    
    assert hashed != password
    assert verify_password(
        password,
        hashed,
    )


def test_wrong_password():

    hashed = password_hash(
        "123456"
    )

    assert not verify_password(
        "wrong",
        hashed
    )


def test_create_access_token():

    token = create_access_token(
        {
            "sub": "1"
        }
    )

    assert token is not None
    assert isinstance(token, str)