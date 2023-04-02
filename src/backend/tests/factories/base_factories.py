import factory

from app.models.base_model import BaseModel


class BaseModelFactory(factory.Factory):
    class Meta:
        abstract = True
        model = BaseModel

    id = factory.Faker("uuid4", cast_to=None)  # noqa: A003
