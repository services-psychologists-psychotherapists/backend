import pytest

from rest_framework.test import APIClient


@pytest.fixture
def guest_client():
    return APIClient()
