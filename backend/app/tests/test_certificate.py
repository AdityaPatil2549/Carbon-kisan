def test_verify_certificate_invalid(client):
    response = client.get("/verify/invalid-id")
    assert response.status_code == 200
    assert response.json()["valid"] == False

def test_verify_certificate_format(client):
    # This just ensures the endpoint doesn't crash on a valid-looking UUID that isn't in DB
    response = client.get("/verify/12345678-1234-1234-1234-123456789012")
    assert response.status_code == 200
    assert response.json()["valid"] == False
