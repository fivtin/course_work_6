## Курсовая работа
### Основы веб-разработки на Django

Реализация проекта сервиса рассылок - системы, автоматически отправляющей электронные письма клиентам с заданной периодичностью.
Пользователи сервиса ведут свои списки клиентов, сообщений и создают рассылки в которой выбранное сообщение отравляется выбранным клиентам.
Сообщения начинают отправляться когда текущее время становится больше время запуска рассылки и завершает отправку сообщений, когда текущее время становится больше времени её завершения.

Для начала пользования сервисом необходимо:

1. Установить зависимости проекта
2. В корневом каталоге проекта создать файл ___.env___ (или переименуйте __.env.sample__) и установите необходимые значения переменных.
3. Выполните миграции командой: ___python3 manage.py migrate___
4. Загрузите данные из фикстур выполнив __python3 manage.py loaddata data.json__
5. Запустите сервер командой ___python3 manage.py runserver___ и перейдите на главную страницу __http://127.0.0.1:8000__
6. Логин и пароль администратора __admin@example.com__ и __123456__ (не забудьте поменять пароль при первом запуске приложения).

Для ручного запуска отправки рассылок выполните команду __python manage.py start_newsletters__
