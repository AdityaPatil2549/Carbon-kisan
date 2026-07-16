import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def dev_farmer_token():
    # Matches _DEV_FARMER_PATTERN
    return "dev_farmer_12345678-1234-1234-1234-123456789012"

@pytest.fixture
def dev_buyer_token():
    # Matches _DEV_BUYER_PATTERN
    return "dev_buyer_12345678-1234-1234-1234-123456789012"

@pytest.fixture
def auth_headers(dev_farmer_token):
    return {"Authorization": f"Bearer {dev_farmer_token}"}

@pytest.fixture
def buyer_headers(dev_buyer_token):
    return {"Authorization": f"Bearer {dev_buyer_token}"}
