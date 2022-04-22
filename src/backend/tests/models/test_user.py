from app.models.user import User


def test_attributes():
    email = "some@email.com"
    username = "some name"
    password = "some password"

    bm = User(email=email, username=username, password=password)

    assert hasattr(bm, "id")
    assert hasattr(bm, "username")
    assert hasattr(bm, "email")
    assert hasattr(bm, "password")
