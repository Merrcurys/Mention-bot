import sqlite3 as sq
from contextlib import closing


class BotDatabase:
    def __init__(self):
        self.conn = sq.connect("data.db")
        
        # создаем таблицы
        self._create_users_table()
        self._create_chats_table()
        self._create_userschats_table()

    # --------функции выборки--------
    def get_all_users(self, chat):
        with closing(self.conn.cursor()) as cursor:
            query = '''SELECT User_ID FROM UsersChats WHERE Chat_ID = ?'''
            cursor.execute(query, (chat,))
            return [member[0] for member in cursor]

    def get_position_tb(self, chat):
        with closing(self.conn.cursor()) as cursor:
            query = '''SELECT Mentions_Tb FROM Chats WHERE ID_Chat = ?'''
            cursor.execute(query, (chat,))
            return cursor.fetchall()[0]

    # --------функции добавления--------
    def add_chat_db(self, chat, m_tb=1):
        with closing(self.conn.cursor()) as cursor:
            query = '''REPLACE INTO Chats (ID_Chat, Mentions_Tb) VALUES(?, ?)'''
            cursor.execute(query, (chat, m_tb))
            self.conn.commit()

    def add_users_db(self, chat, users):
        with closing(self.conn.cursor()) as cursor:
            for user in users:
                query = '''REPLACE INTO Users (ID_User) VALUES(?)'''
                cursor.execute(query, (user,))
                query = '''INSERT INTO UsersChats (User_ID, Chat_ID) VALUES(?, ?)'''
                cursor.execute(query, (user, chat))
                self.conn.commit()

    # --------функции удаления--------
    def del_chat_db(self, chat):
        with closing(self.conn.cursor()) as cursor:
            query = '''DELETE FROM Chats WHERE ID_Chat = ?'''
            cursor.execute(query, (chat,))
            self.conn.commit()

    def del_users_from_chat_db(self, chat, users):
        with closing(self.conn.cursor()) as cursor:
            for user in users:
                query = '''DELETE FROM UsersChats WHERE Chat_ID = ? and User_ID = ?'''
                cursor.execute(query, (chat, user))
                self.conn.commit()

    # --------тумблер--------
    def update_mentions_tb(self, chat, m_tb):
        with closing(self.conn.cursor()) as cursor:
            query = '''UPDATE Chats SET Mentions_Tb = ? WHERE ID_Chat = ?'''
            cursor.execute(query, (m_tb, chat))
            self.conn.commit()

    # --------создание таблиц--------
    def _create_users_table(self):
        with closing(self.conn.cursor()) as cursor:
            query = '''CREATE TABLE IF NOT EXISTS Users (ID_User INTEGER PRIMARY KEY)'''
            cursor.execute(query)
            self.conn.commit()

    def _create_chats_table(self):
        with closing(self.conn.cursor()) as cursor:
            query = '''
                CREATE TABLE IF NOT EXISTS Chats (
                    ID_Chat INTEGER PRIMARY KEY,
                    Mentions_Tb INTEGER)'''
            cursor.execute(query)
            self.conn.commit()

    def _create_userschats_table(self):
        with closing(self.conn.cursor()) as cursor:
            query = '''
                CREATE TABLE IF NOT EXISTS UsersChats (
                    ID_UserChat INTEGER PRIMARY KEY AUTOINCREMENT,
                    User_ID INTEGER NOT NULL,
                    Chat_ID INTEGER NOT NULL,
                    UNIQUE(User_ID, Chat_ID),
                    FOREIGN KEY (User_ID) REFERENCES Users(ID_User),
                    FOREIGN KEY (Chat_ID) REFERENCES Chats(ID_Chat))'''
            cursor.execute(query)
            self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == '__test__':
    db = BotDatabase()
    db.close()
