from fastapi.testclient import TestClient
from src.app import app
client = TestClient(app)

def test_execute_ok():
    r = client.post("/execute", json={"goal": "Reemitir cartao"})
    assert r.status_code == 200
    data = r.json()
    assert data["summary"].startswith("Goal:")
