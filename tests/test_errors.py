def test_404_html_error(client):
    """Tests custom 404 page for browser requests."""
    response = client.get("/nonexistent-page-url")
    assert response.status_code == 404
    assert b"Destination Not Found (404)" in response.data
    assert b"Return to Homepage" in response.data


def test_404_json_api_error(client):
    """Tests JSON error response for API requests."""
    response = client.get("/api/nonexistent-endpoint")
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert data["success"] is False
    assert "not found" in data["error"].lower()
