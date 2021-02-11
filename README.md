# Проект клиент для чата на asyncio

Ситуация такова:

Баба Зина ведёт двойную жизнь. Днём она печёт пирожки, гуляет с внуками и вяжет на спицах, а ночью – виртуозно строит в Майнкрафт фермы и курятники. Детство в деревне – это вам не кусь кошачий.

На днях по Майнкрафт-сообществу прошла радостная новость: несколько умельцев создали чат для обмена кодами. Анонимный, история сообщений не сохраняется, войти и выйти можно в любой момент. Идеальное место для читеров.

Баба Зина просто обязана в него попасть! Иначе и лидерство по району потерять недолго. Вот только пользоваться компьютером за пределами Майнкрафта она умеет не очень хорошо.


В репозитории два скрипта:
- Скрипт просмотра чата:
    * Подключается к чату.
    * Сохраняет историю переписки.    
- Скрипт отправки сообщения:
    * Позволяет включиться в переписку.
Для отправки сообщений нужна регистрация - имя для получения токена.
При регистрации токен сохраняется в конфигурационном файле
 и при повторном запуске авторизуется по этому токену.


## Для работы требуется:
- python 3.7
- установка зависимостей командой `pip -r requirements.txt` из корня папки. (либо pip3/pip3.x)

## Запуск:
`$ python listen-minechat.py --host 192.168.0.1 \
--port 5001 --log_path ~/minechat.history` (либо python3/python3.x)

`$ python send_message.py --host 192.168.0.1 \
--port 5001 --message "Hello!"` (либо python3/python3.x)

Список аргументов скрипта просмотра сообщений:
* host - адрес ресурса к которому нужно подключиться (необязателен).
* port - порт ресурса к которому нужно подключиться (необязателен).
* log_path - путь к файлу с историей переписки (необязателен).

Список аргументов скрипта для посылки собщений:
* host - адрес ресурса к которому нужно подключиться (необязателен).
* port - порт ресурса к которому нужно подключиться (необязателен).
* log_path - путь к файлу с для хранения служебной информации (необязателен).
* token - токен для входа в чат (необязателен).
* name - имя для регистрации (необязателен).
* message - сообщение в чат (обязателен).


# Аргументы прописываются:
- в консоли после имени скрипта, например `--host 0.0.0.0`.
- или в файле конфигурации (по-умолчанию `listener_config.cfg` - для скрипта просмотра сообщений
и `sender_config.txt` - для скрипта отсылки сообщения в чат).
пример:
```
host=0.0.0.0
post=8000
``` 



Проект сделан в учебных целям в рамках проекта [Девман](dvmn.org)
