from pytest_factoryboy import register

from tests.factories.todo_factory import TodoFactory
from tests.factories.user_factory import UserFactory

register(UserFactory)
register(TodoFactory)
