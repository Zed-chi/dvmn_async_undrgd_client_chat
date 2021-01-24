# Проект клиент для чата на asyncio

Ситуация такова:
```
    Баба Зина ведёт двойную жизнь. Днём она печёт пирожки, гуляет с внуками и вяжет на спицах, а ночью – виртуозно строит в Майнкрафт фермы и курятники. Детство в деревне – это вам не кусь кошачий.

    На днях по Майнкрафт-сообществу прошла радостная новость: несколько умельцев создали чат для обмена кодами. Анонимный, история сообщений не сохраняется, войти и выйти можно в любой момент. Идеальное место для читеров.

    Баба Зина просто обязана в него попасть! Иначе и лидерство по району потерять недолго. Вот только пользоваться компьютером за пределами Майнкрафта она умеет не очень хорошо.
```

Программа:
 * Подключается к чату.
 * Сохраняет историю переписки.
 * Позволяет включиться в переписку.


## Для работы требуется:
- python 3.7
- установка зависимостей командой `pip -r requirements.txt` из корня папки. (либо pip3/pip3.x)

## Запуск:
`$ python listen-minechat.py --host 192.168.0.1 \
--port 5001 --history_path ~/minechat.history` (либо python3/python3.x)

Список аргументов скрипта просмотра сообщений:
* host - адрес ресурса к которому нужно подключиться (обязателен).
* port - порт ресурса к которому нужно подключиться (обязателен).
* history_path - путь к файлу с историей переписки (необязателен).

Список аргументов скрипта для посылки собщений:
* host - адрес ресурса к которому нужно подключиться (обязателен).
* sender_port - порт ресурса к которому нужно подключиться (обязателен).
* sender_log_path - путь к файлу с для хранения служебной информации (необязателен).
* token - токен для входа в чат (необязателен).
* name - имя для регистрации (необязателен).


# Аргументы прописываются:
- в файле `config.txt` без тире.
    ```
    host=...
    post=...
    ``` 
- либо в консоли после имени скрипта.


Проект сделан в учебных целям в рамках проекта [Девман](dvmn.org)