import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = False  # keep real error handlers active
    return app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "healthy"}


def test_chat_success(client):
    r = client.post("/api/chat", json={"message": "How can I manage my monthly budget?"})
    assert r.status_code == 200
    assert "response" in r.get_json()


def test_empty_message_rejected(client):
    r = client.post("/api/chat", json={"message": "   "})
    assert r.status_code == 400


def test_missing_message_rejected(client):
    r = client.post("/api/chat", json={"text": "hi"})
    assert r.status_code == 400


def test_invalid_json(client):
    r = client.post("/api/chat", data="{not json", content_type="application/json")
    assert r.status_code == 400
    assert "Traceback" not in r.get_data(as_text=True)


def test_too_long_message_rejected(client):
    r = client.post("/api/chat", json={"message": "a" * 501})
    assert r.status_code == 413


@pytest.mark.parametrize("bad", [123, ["a"], {"x": 1}, True])
def test_unexpected_type_rejected(client, bad):
    r = client.post("/api/chat", json={"message": bad})
    assert r.status_code == 400


def test_security_headers_present(client):
    r = client.get("/health")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in r.headers


def test_unknown_route_is_json_404(client):
    r = client.get("/nope")
    assert r.status_code == 404
    assert r.get_json() == {"error": "Not found."}
