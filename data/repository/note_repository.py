from domain.model.note import Note
from data.model.note import Note as DBNote
from typing import List


class NoteRepository():

    async def create_note_and_return(self, title: str, body: str, user_id: int):
        note_obj = DBNote(title=title, body=body, user_id=user_id)

        await note_obj.save()

        print(note_obj.id)

        return Note(
            id=note_obj.id,
            title=note_obj.title,
            body=note_obj.body,
            created_at=note_obj.created_at,
            updated_at=note_obj.updated_at,
            user_id=user_id
        )

    async def get_all_notes(self, user_id: int) -> List[Note]:
        try:
            notes_obj = await DBNote.get(user_id=user_id)
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
        except:
            return []

    async def get_note_by_id(self, note_id: int, user_id: int):
        try:
            note_obj = await DBNote.get(id=note_id, user_id=user_id)

            return Note(
                id=note_obj.id,
                title=note_obj.title,
                body=note_obj.body,
                created_at=note_obj.created_at,
                updated_at=note_obj.updated_at,
                user_id=user_id
            )
        except:
            return None

    async def update_note(self, note: Note, user_id: int):
        try:
            updated_note = note.dict().copy()
            updated_note.pop('id')
            updated_note.pop('created_at')
            updated_note.pop('updated_at')
            updated_note.pop('user_id')
            note_obj = await DBNote.filter(id=note.id, user_id=user_id).update(**updated_note)
        except Exception:
            raise Exception
            pass

    async def delete_note(self, note_id: int, user_id: int):
        try:
            await DBNote.filter(id=note_id, user_id=user_id).delete()
        except:
            pass
