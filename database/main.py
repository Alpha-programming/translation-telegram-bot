import sqlite3
from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent

class DatabaseConnection:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.cursor, self.connection = self.connect()


    def connect(self) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
        connection = sqlite3.connect(BASE_DIR / self.database_path)
        cursor = connection.cursor()
        return cursor, connection

class DatabaseTables(DatabaseConnection):
    def __init__(self, database_path: str) -> None:
        super().__init__(database_path)

    def create(self, query:str) -> None:
        self.cursor.executescript(query)

db_table = DatabaseTables('translations.db')
db_table.create("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id BIGINT UNIQUE
);

CREATE TABLE IF NOT EXISTS translations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lang_from TEXT,
    lang_To TEXT,
    original TEXT,
    translated TEXT,
    created_at DATE,
    user_id INTEGER REFERENCES users(id)
);
""")

class UsersRepo(DatabaseConnection):
    def get_user(self, chat_id: int) -> tuple | None:
        self.cursor.execute("SELECT id FROM users WHERE chat_id = ?;", (chat_id,))
        result = self.cursor.fetchone()
        return result

    def add_user(self, chat_id:int) -> None:
        query = 'INSERT INTO users(chat_id) VALUES (?);'

        if self.get_user(chat_id) is None:
            self.cursor.execute(query, (chat_id,))
            self.connection.commit()

from datetime import datetime

class TranslationRepo(DatabaseConnection):
    def add_translation(self,
                        lang_from:str,
                        lang_to:str,
                        original:str,
                        translated:str,
                        created_at:datetime,
                        user_id:int
                        )->None:
        query = ('''INSERT INTO translations(lang_from,lang_to,original,translated,created_at,user_id)
                 VALUES(?,?,?,?,?,?);
                 ''')

        self.cursor.execute(query,(lang_from,lang_to,original,translated,created_at,user_id))
        self.connection.commit()

class HistoryRepo(DatabaseConnection):
    def get_history(self, user_id) -> tuple | None:
        query = 'SELECT lang_from,lang_to,original,translated,created_at,id FROM translations where user_id =?;'
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def delete_history(self, _id) -> None:
        query = 'DELETE FROM translations WHERE id = ?;'
        self.cursor.execute(query,(_id,))

users_repo = UsersRepo(BASE_DIR/'translations.db')
translations_repo = TranslationRepo(BASE_DIR/'translations.db')
history_repo = HistoryRepo(BASE_DIR/'translations.db')




