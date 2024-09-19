<p align="center">
      <img src="https://i.ibb.co/2nW3Bq7/avatar6517195165-2-out-1.jpg" alt="Project Logo" width="726">
</p>

## О боте
Mention bot - это бот, который может оповещать всех пользователей в чате.

Бота можно найти и протестировать по этому адресу: [@fast_mention_bot](https://t.me/fast_mention_bot?start=c1686051798545-ds)

## Функционал бота
1. `/help`, `/command` - справка по всем командам.

2. `/all`, `/here`, `/everyone` - позвать всех пользователей. 

3. `/access_toggle` - тумблер прав доступа к оповещениям.

4. `/names_visibility` - тумблер для видимости имен при оповещении.

5. Все ошибки бот отправляет в админский чат.

## Ограничения бота
* Бот работает только до 75 участников.
* Команду `/all` нельзя вызывать в одном чате, чаще чем раз в минуту.
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
API_ID = <получить можно на https://my.telegram.org>
API_HASH = <получить можно на https://my.telegram.org>
ADMIN_CHAT_ID = <скопируйте последние цифры в адрессной строки в браузере>
```
Запуск бота
```
python main.py
```
