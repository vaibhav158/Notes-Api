from src.dependencies.auth import get_current_user, get_app_settings
from data.repository.note_repository import NoteRepository
from domain.model.user import User
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pydantic import BaseModel
from domain.model.note import Note
import traceback

note_router = APIRouter(prefix='/note', tags=['note'])


class NoteCreateRequest(BaseModel):
    title: str
    body: str


class NoteUpdateRequest(BaseModel):
    id: int
    title: str
    body: str


@note_router.post('/create')
async def create_note(
    note: NoteCreateRequest,
    user: User = Depends(get_current_user),
    repository: NoteRepository = Depends()
):
    return await repository.create_note_and_return(title=note.title, body=note.body, user_id=user.id)


@note_router.patch('/update')
async def update_note(
    note: NoteUpdateRequest,
    user: User = Depends(get_current_user),
    repository: NoteRepository = Depends(),
):
    try:
        return await repository.update_note(note_id=note.id, title=note.title, body=note.body, user_id=user.id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Note doesn't exists"
        )


@note_router.delete('/delete')
async def delete_note(
    id: int,
    user: User = Depends(get_current_user),
    repository: NoteRepository = Depends()
):
    try:
        return await repository.delete_note(note_id=id, user_id=user.id)
    except:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Note doesn't exists"
        )


@note_router.get('/all')
async def get_all_notes(
    user: User = Depends(get_current_user),
    note_repository: NoteRepository = Depends()
):
    try:
        return await note_repository.get_all_notes(user_id=user.id)
    except:
        return []


@note_router.get('/{id}')
async def get_note_by_id(
    id: int,
    user: User = Depends(get_current_user),
    note_repository: NoteRepository = Depends()
):
    try:
        return await note_repository.get_note_by_id(note_id=id, user_id=user.id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Note doesn't exists"
        )
