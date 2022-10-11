import pytest
from django.core.exceptions import ValidationError

from transactions.models import Room

"""
START FIXTURES
"""


@pytest.fixture
def room():
    return Room(
        name="Test room",
        capacity=10
    )


@pytest.fixture
def room_with_zero_capacity():
    return Room(
        name="Test room 2",
        capacity=0
    )


"""
END FIXTURES
"""


class TestRoom:
    def test_room(self, room):
        assert room.name is not ""
        assert room.name is not None
        assert room.capacity is not None

    def test_room_with_zero_capacity(self, room_with_zero_capacity):
        with pytest.raises(ValidationError) as validation_error:
            room_with_zero_capacity.full_clean()
        assert 'capacity' in validation_error.value.message_dict
