import factory

from app.models.user import User
from tests.factories.base_factories import BaseModelFactory


class UserFactory(BaseModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
