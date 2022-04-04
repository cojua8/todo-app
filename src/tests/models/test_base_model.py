from app.models.base_model import BaseModel


def test_attributes():
    bm = BaseModel()

    assert hasattr(bm, "id")
