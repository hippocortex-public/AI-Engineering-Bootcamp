from pathlib import Path
import subprocess

import yaml

LAB = Path(__file__).resolve().parents[2]


def test_compose_network_ports_secrets_and_dependencies():
    data = yaml.safe_load((LAB / "compose.yaml").read_text())
    api, db, redis = (data["services"][name] for name in ("api", "db", "redis"))
    assert "ports" not in db and "ports" not in redis
    assert api["ports"] == ["127.0.0.1:8000:8000"]
    assert data["networks"]["backend"]["internal"] is True
    assert api["read_only"] is True and api["cap_drop"] == ["ALL"]
    assert "db_admin_password" not in api["secrets"]
    assert api["depends_on"]["db"]["condition"] == "service_healthy"
    assert api["depends_on"]["redis"]["condition"] == "service_healthy"
    assert "pg_data" in data["volumes"] and "redis_data" in data["volumes"]


def test_container_uses_unprivileged_user_and_exec_form():
    dockerfile = (LAB / "Dockerfile").read_text()
    assert "USER 10001:10001" in dockerfile
    assert 'CMD ["python", "-m", "uvicorn"' in dockerfile
    assert "--reload" not in dockerfile
    assert "configure_demo" not in dockerfile


def test_shell_bootstrap_syntax():
    for name in ("postgres/001-init.sh", "redis/bootstrap.sh"):
        subprocess.run(["sh", "-n", str(LAB / name)], check=True)


def test_build_context_does_not_include_secrets_or_tests():
    patterns = (LAB / ".dockerignore").read_text().splitlines()
    assert patterns[0] == "*"
    assert "!requirements.txt" in patterns
    assert not any("secrets" in p and p.startswith("!") for p in patterns)
