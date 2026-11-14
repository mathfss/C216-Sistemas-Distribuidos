def test_cors_allowed_origin(client):
    response = client.get(
        "/items",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_unallowed_origin(client):
    response = client.get(
        "/items",
        headers={"Origin": "http://origem-desconhecida.com"},
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers

