import sqlite3 as sq


# создает таблицы, если они еще не созданы.
def create_data():
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Users (ID_Users INTEGER PRIMARY KEY)""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Chats (ID_Chats INTEGER PRIMARY KEY)""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS UsersChats (
            ID_UsersChats INTEGER PRIMARY KEY AUTOINCREMENT,
            Users_ID INTEGER NOT NULL,
            Chats_ID INTEGER NOT NULL,
            UNIQUE(Users_ID, Chats_ID),
            FOREIGN KEY (Users_ID) REFERENCES Users(ID_Users),
            FOREIGN KEY (Chats_ID) REFERENCES Chats(ID_Chats))""")


# функция возращает список кортежей. в кортеже возращается id чата, пользователя.
def return_users_db(chat):
    create_data()
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            "SELECT Users_ID FROM UsersChats WHERE Chats_ID = ?", (chat,))
        members = [member[0] for member in cur]
        return members


# функция записывает в БД пользователя, его группу
def reg_users_db(chat, users):
    create_data()
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            "REPLACE INTO Chats (ID_Chats) VALUES(?)", (chat,))
        for user in users:
            cur.execute(
                "REPLACE INTO Users (ID_Users) VALUES(?)", (user,))
            cur.execute(
                "REPLACE INTO UsersChats (Users_ID, Chats_ID) VALUES(?, ?)", (user, chat))


def delete_users_db(chat, users):  # функция удаляет из БД пользователей
    create_data()
    with sq.connect("data.db") as con:
        cur = con.cursor()
        for user in users:
            cur.execute(
                "DELETE FROM UsersChats WHERE Chats_ID = ? and Users_ID = ?", (chat, user))


