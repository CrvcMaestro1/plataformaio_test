import datetime

import pytest

from transactions.models import Event, Room

"""
START FIXTURES
"""


@pytest.fixture
def room():
    return Room(
        name="Test room",
        capacity=2
    )


@pytest.fixture
def event(room):
    return Event(
        room=room,
        day=datetime.date(2022, 10, 10),
        name="Test event",
        is_public=True
    )


"""
END FIXTURES
"""


class TestEvent:
    def test_event(self, event):
        assert event.name is not ""
        assert event.name is not None
        assert event.is_public is True
