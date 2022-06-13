from httpx import AsyncClient
from httpx import Response
import pytest
from src.main import app
from data.model.user import User
from src.dependencies.auth import get_current_user
from typing import List
from domain.model.note import Note


async def override_get_current_user():
    return await User.get(username="test1")


app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.anyio
async def test_get_note_by_id_successful(client: AsyncClient):
    await create_test_user(client)
    await create_test_note(client)

    response = await client.get(f'/note/{1}')

    assert response.status_code == 200

    assert response.json()["title"] == "Test Note1"  


@pytest.mark.anyio
async def test_get_note_by_id_no_note_exists(client: AsyncClient):
    await create_test_user(client)
    await create_test_note(client)

    response = await client.get(f'/note/{10}')

    assert response.status_code == 400    


@pytest.mark.anyio
async def test_create_note_success(client: AsyncClient):

    await create_test_user(client)

    note_json = {"title": "Test Note1",
                 "body": "Hey, This is my First Test Note"}
    response = await client.post('/note/create', json=note_json)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_note_null_title_body(client: AsyncClient):
    await create_test_user(client)

    json = {"title": None, "body": None}
    response = await client.post('/note/create', json=json)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_note_null_title(client: AsyncClient):
    await create_test_user(client)

    json = {"title": None, "body": "Hey, This is my First Test Note"}
    response = await client.post('/note/create', json=json)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_note_null_body(client: AsyncClient):
    await create_test_user(client)

    json = {"title": "None", "body": None}
    response = await client.post('/note/create', json=json)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_update_note_successful(client: AsyncClient):
    await create_test_user(client)
    await create_test_note(client)

    json = {"id": 1, "title": "Updated Test Note1",
            "body": "Updated Test Note body"}
    response = await client.patch('/note/update', json=json)

    assert response.status_code == 200


@pytest.mark.anyio
async def test_update_note_no_note_exists(client: AsyncClient):

    json = {"id": 10, "title": "Updated Test Note1",
            "body": "Updated Test Note body"}
    response = await client.patch('/note/update', json=json)

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Note doesn't exists"
    }


@pytest.mark.anyio
async def test_delete_note_successful(client: AsyncClient):
    await create_test_user(client)
    await create_test_note(client)

    response = await client.delete(f'/note/delete?id={1}')

    assert response.status_code == 200


@pytest.mark.anyio
async def test_delete_note_no_note_exists(client: AsyncClient):
    await create_test_user(client)
    await create_test_note(client)

    response = await client.delete(f'/note/delete?id={10}')

    assert response.status_code == 400


@pytest.mark.anyio
async def test_note_get_all_success(client: AsyncClient):

    await create_test_user(client)
    await create_test_note(client)

    response = await client.get('/note/all')

    assert response.status_code == 200

    notes: List[Note] = response.json()
    assert len(notes) > 0


async def create_test_user(client: AsyncClient):
    user = {"username": "test1", "password": "mytestpassword"}
    await client.post('/auth/register', json=user)


async def create_test_note(client: AsyncClient):
    note_json = {"title": "Test Note1",
                 "body": "Hey, This is my First Test Note"}
    await client.post('/note/create', json=note_json)
