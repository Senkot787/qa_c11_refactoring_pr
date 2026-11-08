import os
import pytest
import requests
from api_client import CourierAPIClient

@pytest.fixture
def client():
    base_url = os.getenv("API_BASE_URL")
    auth_token = os.getenv("AUTH_TOKEN")
    return CourierAPIClient(base_url, auth_token)

@pytest.fixture
def new_courtier_data():
    return {
        "first_name": "Мария",
        "last_name": "Сидорова",
        "phone": "+79997654321"
    }

@pytest.mark.usefixtures("fake_server")
class TestCourierHelpers:

    def test_get_courier_by_id(self, client):
        courier = client.get_courier_by_id(1)
        assert courier["id"] == 1
        assert courier["first_name"] == "Иван"

    def test_create_courier(self, client, new_courtier_data):
        result = client.create_courier(new_courtier_data)
        assert "id" in result
        assert result["first_name"] == "Мария"

    def test_get_nonexistent_courier_raises(self, client):
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_courier_by_id(99999)

    def test_delete_courier(self, client):
        result = client.delete_courier(2)
        assert result == {"status": "deleted"}