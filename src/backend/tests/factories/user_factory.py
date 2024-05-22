import factory

from app.domain.models.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker("uuid4", cast_to=None)
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
