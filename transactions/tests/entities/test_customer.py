import pytest

from transactions.models import Customer

"""
START FIXTURES
"""


@pytest.fixture
def customer():
    return Customer(
        name="Christian"
    )


"""
END FIXTURES
"""


class TestCustomer:
    def test_customer(self, customer):
        assert customer.name is not ""
        assert customer.name is not None
