import json
from pathlib import Path
import httpx


def main():
    raw = json.loads((Path(__file__).resolve().parent / "secrets/api_identities.json").read_text())
    keys = {i["subject"]: i["api_key"] for i in raw}
    alpha, ops = {"X-API-Key": keys["alice"]}, {"X-API-Key": keys["operator"]}
    with httpx.Client(base_url="http://127.0.0.1:8000", timeout=10, trust_env=False) as c:
        assert c.get("/health/live").status_code == 200
        assert c.get("/health/ready").status_code == 200
        assert c.post("/chat", json={"message": "Bonjour"}).status_code == 401
        assert c.get("/documents/alpha-guide", headers=alpha).status_code == 200
        assert c.get("/documents/beta-guide", headers=alpha).status_code == 404
        payload = {"message": "Résume le guide", "document_id": "alpha-guide"}
        assert c.post("/chat", json=payload, headers=alpha).status_code == 200
        response = c.post("/chat", json=payload, headers=alpha)
        assert response.status_code == 200 and response.json()["cached"] is True
        assert c.get("/metrics", headers=alpha).status_code == 403
        metrics = c.get("/metrics", headers=ops)
        assert metrics.status_code == 200 and "ai_http_requests_total" in metrics.text
    print("9 contrôles de livraison réussis, sans affichage de secrets.")


if __name__ == "__main__":
    main()
