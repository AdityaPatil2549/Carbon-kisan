def test_public_districts(client):
    response = client.get("/auth/districts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_impact_stats(client):
    response = client.get("/impact/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_co2e_listed" in data
    assert "top_districts" in data
    assert isinstance(data["top_districts"], list)

def test_browse_listings(client):
    response = client.get("/listings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
