import pytest
from django.contrib.auth.models import User
import json

@pytest.mark.django_db
def test_api_route_login(client):
    User.objects.create_user(username="hosty", password="123456")

    response = client.post("/api/login/", {"username": "hosty", "password": "123456"})
    assert response.status_code == 200

@pytest.mark.django_db
def test_api_route_logout(client):
    test_api_route_login(client)

    response = client.post('/api/logout/')
    assert response.status_code == 500

@pytest.mark.django_db
def test_api_route_pecas_list(client):

    test_api_route_login(client)

    response = client.get('/api/pecas/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_api_route_pecas_create(client):

    test_api_route_login(client)

    response = client.post('/api/pecas/', {
        "name": "Cabecote",
        "code": "12356gghjn",
        "description": "Sensor do motor",
        "amount": 1
    })
    assert response.status_code == 201

@pytest.mark.django_db
def test_api_route_pecas_update(client):
    test_api_route_login(client)

    headers = {"Content-Type": "application/json"}

    response_create = client.post('/api/pecas/', {
        "name": "Cabecote",
        "code": "12356gghjn",
        "description": "Sensor do motor",
        "amount": 1
    })

    assert response_create.status_code == 201

    dataPut = {
        "name": "Vira Brequim",
        "code": "kjsadfn223",
        "description": "Roda a roda2",
        "amount": 120
    }
    
    response = client.put(f'/api/pecas/{response_create.data['id']}/', 
        json.dumps(dataPut), 
        headers=headers
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_api_route_pecas_retrieve(client):
    test_api_route_login(client)

    response_create = client.post('/api/pecas/', {
        "name": "Cabecote",
        "code": "12356gghjn",
        "description": "Sensor do motor",
        "amount": 1
    })
    assert response_create.status_code == 201

    response = client.get(f'/api/pecas/{response_create.data['id']}/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_api_route_pecas_delete(client):
    test_api_route_login(client)

    response_create = client.post('/api/pecas/', {
        "name": "Cabecote",
        "code": "12356gghjn",
        "description": "Sensor do motor",
        "amount": 1
    })
    assert response_create.status_code == 201

    response = client.delete(f'/api/pecas/{response_create.data['id']}/')

    assert response.status_code == 200
