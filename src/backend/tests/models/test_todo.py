import datetime as dt
from uuid import UUID, uuid4

import freezegun

from app.models.todo import Todo


@freezegun.freeze_time(
    "2022-04-04",
)
def test_attributes():
    due_date = dt.datetime.now(tz=dt.UTC).date()
    owner_id = uuid4()
    description = "test"

    bm = Todo(owner_id=owner_id, description=description, due_date=due_date)

    assert isinstance(bm.id, UUID)
    assert bm.owner_id == owner_id
    assert bm.description == description
    assert bm.due_date == due_date
    assert bm.completed is False
    assert bm.date_created == dt.datetime.now(tz=dt.UTC).date()
