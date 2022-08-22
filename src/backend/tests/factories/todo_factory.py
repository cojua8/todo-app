import factory
from app.models.todo import Todo
from tests.factories.base_factories import BaseModelFactory


class TodoFactory(BaseModelFactory):
    class Meta:
        model = Todo

    owner_id = factory.Faker("uuid4", cast_to=None)
    description = factory.Faker("paragraph")
    due_date = factory.Faker("date_object")
    completed = False
    date_created = factory.Faker("date_object")
