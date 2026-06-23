import sys, traceback
sys.path.insert(0, ".")

try:
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.post(
        "/predict/mhtcet",
        json={
            "percentile": 88.5,
            "category": "GOPENS",
            "home_university": "Sant Gadge Baba Amravati University",
        },
    )
    print("STATUS:", resp.status_code)
    print("BODY:", resp.text[:1000])
except Exception:
    print("CRASHED OUTSIDE REQUEST:")
    traceback.print_exc()