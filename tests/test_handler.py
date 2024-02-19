import pytest
from sanic_testing.reusable import ReusableClient  # type:ignore

from grabbers.app import app as sanic_app


@pytest.fixture
def client():
    with ReusableClient(sanic_app) as client:
        yield client


def test_index(client):
    request, response = client.get("/")
    assert response.status == 200
    assert "Welcome" in response.text
    request, response = client.get("")
    assert response.status == 200
    assert "Welcome" in response.text


def test_get(client):
    request, response = client.get("/qq.com")

    assert request.method.lower() == "get"
    assert response.status == 200
    assert "https://new.qq.com" in response.text

    request, response = client.get("/http://qq.com")
    assert response.status == 200
    assert "https://new.qq.com" in response.text

    request, response = client.get("/http.qq.com")
    assert response.status == 200
    assert "https://new.qq.com" in response.text

    request, response = client.get("/http:qq.com?a=1")
    assert response.status == 200
    assert "https://new.qq.com" in response.text

    request, response = client.get("/https://news.qq.com/ch/auto/")
    assert response.status == 200
    assert "//i.news.qq.com" in response.text
