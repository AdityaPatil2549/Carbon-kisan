def test_estimate_valid_request(client, auth_headers):
    payload = {
        "practice_type": "no_till",
        "area_ha": 5.0,
        "district_code": "MH_PUNE",
        "season_months": 12
    }
    response = client.post("/estimate", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "estimate_id" in data
    assert "co2e_tonnes" in data
    assert "shap_breakdown" in data
    assert "inr_estimate" in data

def test_estimate_invalid_area(client, auth_headers):
    payload = {
        "practice_type": "no_till",
        "area_ha": 15.0, # PRD says max 10
        "district_code": "MH_PUNE",
        "season_months": 12
    }
    response = client.post("/estimate", json=payload, headers=auth_headers)
    assert response.status_code == 422 # Validation error

def test_estimate_unauthorized(client):
    payload = {
        "practice_type": "no_till",
        "area_ha": 5.0,
        "district_code": "MH_PUNE",
        "season_months": 12
    }
    response = client.post("/estimate", json=payload)
    assert response.status_code == 401
