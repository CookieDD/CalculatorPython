from fastapi.testclient import TestClient
import pytest

from Calculator import app, _safe_eval


client = TestClient(app)


def test_safe_eval_basic():
    assert _safe_eval("2+3") == 5


def test_safe_eval_unary():
    assert _safe_eval("-5") == -5


def test_safe_eval_pow():
    assert _safe_eval("2**3") == 8


def test_safe_eval_invalid_name():
    with pytest.raises(ValueError):
        _safe_eval("__import__('os').system('ls')")


def test_safe_eval_non_numeric_constant():
    with pytest.raises(ValueError):
        _safe_eval("'hello'")


def test_division_by_zero_api():
    r = client.post("/api/calc", json={"expr": "1/0"})
    assert r.status_code == 400
    assert "division" in r.json().get("detail", "").lower()


def test_api_add():
    r = client.post("/api/calc", json={"op":"add","a":2,"b":3})
    assert r.status_code == 200
    assert r.json()["result"] == 5


def test_api_unknown_op():
    r = client.post("/api/calc", json={"op":"unknown","a":1,"b":2})
    assert r.status_code == 400
