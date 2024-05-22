import factory

from app.domain.models.todo import Todo


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    id = factory.Faker("uuid4", cast_to=None)
    owner_id = factory.Faker("uuid4", cast_to=None)
    description = factory.Faker("paragraph")
    due_date = factory.Faker("date_object")
    completed = False
    date_created = factory.Faker("date_object")
