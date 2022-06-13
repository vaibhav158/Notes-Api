from httpx import AsyncClient
import pytest
from src.auth.routes.auth import UserResponse
from domain.model.user import User


@pytest.mark.anyio
async def test_user_registration_empty_username_password(client: AsyncClient):

    json = { "username": "", "password": "" }
    response = await client.post('/auth/register', json=json)

    assert response.status_code == 400


@pytest.mark.anyio
async def test_user_registration_null_username_password(client: AsyncClient):

    json = { "username": None, "password": None }
    response = await client.post('/auth/register', json=json)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_user_registration_short_username(client: AsyncClient):

    json = { "username": "tes", "password": "mytestpassword" }
    response = await client.post('/auth/register', json=json)

    assert response.status_code == 400


@pytest.mark.anyio
async def test_user_registration_short_password(client: AsyncClient):

    json = { "username": "test1", "password": "my" }
    response = await client.post('/auth/register', json=json)

    assert response.status_code == 400


@pytest.mark.anyio
async def test_user_registration_successful(client: AsyncClient):

    json = { "username": "test1", "password": "mytestpassword" }
    response = await client.post('/auth/register', json=json)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_user_registration_username_unavailable(client: AsyncClient):

    json = { "username": "test1", "password": "mytestpassword" }
    response = await client.post('/auth/register', json=json)

    assert response.status_code == 400

    assert response.json() == {
        "detail": "User with this username already exists"
    }


@pytest.mark.anyio
async def test_login_successful(client: AsyncClient):

    json= { "username": "test1", "password": "mytestpassword" }
    response = await client.post('/auth/login', json=json)

    print(response.json())
    assert response.status_code == 200



@pytest.mark.anyio
async def test_login_wrong_password(client: AsyncClient):

    json= { "username": "test1", "password": "mywrongtestpassword" }
    response = await client.post('/auth/login', json=json)

    print(response.json())
    assert response.status_code == 400



@pytest.mark.anyio
async def test_login_no_user_found(client: AsyncClient):

    json= { "username": "test2", "password": "mytestpassword" }
    response = await client.post('/auth/login', json=json)

    assert response.status_code == 400

    assert response.json() == {
        "detail": "User with this username doesn't exists"
    }


@pytest.mark.anyio
async def test_login_empty_username_password(client: AsyncClient):

    json= { "username": "", "password": "" }
    response = await client.post('/auth/login', json=json)

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Either Username or Passsword is not Valid"
    }


@pytest.mark.anyio
async def test_login_null_username_password(client: AsyncClient):

    json= { "username": None, "password": None }
    response = await client.post('/auth/login', json=json)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_current_user_wrong_token(client: AsyncClient):

    headers = { 'Authorization': 'Bearer svhcjbvjzdbvsdagsncklndvkjnvkndskvnsdklnv' }
    response = await client.get('/auth/user/me', headers=headers)

    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_current_user_successful(client: AsyncClient):
    
    json = { "username": "test1", "password": "mytestpassword" }
    register_response = await client.post('/auth/register', json=json)

    access_token: str = UserResponse(**register_response.json()).token.access_token

    headers = { 'Authorization': f'Bearer {access_token}' }

    response = await client.get('/auth/user/me', headers=headers)

    assert response.status_code == 200

    user = User(**response.json())

    assert user.username == "test1"