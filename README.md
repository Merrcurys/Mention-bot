<p align="center">
      <img src="https://i.ibb.co/2nW3Bq7/avatar6517195165-2-out-1.jpg" alt="Project Logo" width="726">
</p>

## О боте
Mention bot - это бот, который может оповещать всех пользователей в чате.

Бота можно найти и протестировать по этому адресу: @fast_mention_bot

## Функционал бота
1. /start, /command, /help - справка по всем командам.

2. /all, /here, /everyone – оповестить всех пользователей.

3. /mentions_toggle - тумблер для переключения прав доступа к оповещениям

4. Все ошибки бот отправляет в админский чат.

## Ограничения бота
* Бот работает только до 75 участников.
* Команду all нельзя вызывать в одном чате, чаще чем раз в минуту.
* В одном сообщение хранится не больше 5 ссылок на пользователей.

## Установка
Создание виртуального окружения

Для Linux
```
python3 -m venv venv
source venv/bin/activate
```
Для Windows
```
python -m venv venv
venv\Scripts\activate
```
Установка зависимостей:
```
pip install -r requirements.txt
```
Подготовка админского чата:

Добавьте бота в админский чат.

Заполните файл .env
```
API_TOKEN = <получить можно через @BotFather>
BOT_ID = <первые цифры до двоеточия в API_TOKEN>
API_ID = <получить можно на https://my.telegram.org>
API_HASH = <получить можно на https://my.telegram.org>
ADMIN_CHAT_ID = <добавьте бота @getmyid_bot в админский чат, этот бот напишет вам id чата>
```
Запуск бота
```
python main.py
```
