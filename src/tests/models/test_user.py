from app.models.user import User


def test_attributes():
    email = "some@email.com"
    name = "some name"

    bm = User(email=email, name=name)

    assert hasattr(bm, "id")
    assert hasattr(bm, "email")
