from domain.model.note import Note
from data.model.note import Note as DBNote
from typing import List
from tortoise.expressions import Q


class NoteRepository():

    async def create_note_and_return(self, title: str, body: str, user_id: int):
        note_obj = DBNote(title=title, body=body, user_id=user_id)

        await note_obj.save()

        return Note(
            id=note_obj.id,
            title=note_obj.title,
            body=note_obj.body,
            created_at=note_obj.created_at,
            updated_at=note_obj.updated_at,
            user_id=user_id
        )

    async def get_all_notes(self, user_id: int) -> List[Note]:
        notes_obj = await DBNote.filter(user_id=user_id)
        notes = []
        for note_obj in notes_obj:
            notes.append(
                Note(
                    id=note_obj.id,
                    title=note_obj.title,
                    body=note_obj.body,
                    created_at=note_obj.created_at,
                    updated_at=note_obj.updated_at,
                    user_id=user_id
                )
            )
        return notes

    async def get_note_by_id(self, note_id: int, user_id: int):
        note_obj = await DBNote.filter(
            Q(id=note_id) & Q(user_id=user_id)
        ).first()

        return Note(
            id=note_obj.id,
            title=note_obj.title,
            body=note_obj.body,
            created_at=note_obj.created_at,
            updated_at=note_obj.updated_at,
            user_id=user_id
        )

    async def update_note(self, note_id: int, title: str, body: str, user_id: int):
        
        do_note_exists = await self.get_note_by_id(note_id=note_id, user_id=user_id)

        if not do_note_exists:
            raise Exception("Note does not exists")

        updated_note = {
            "title": title,
            "body": body
        }
        await DBNote.filter(
            Q(id=note_id) & Q(user_id=user_id)
        ).update(**updated_note)


    async def delete_note(self, note_id: int, user_id: int):

        do_note_exists = await self.get_note_by_id(note_id=note_id, user_id=user_id)

        if not do_note_exists:
            raise Exception("Note does not exists")

        await DBNote.filter(
            Q(id=note_id) & Q(user_id=user_id)
        ).delete()
