![DjangoLogo](hammerSystems/assets/django-logo.png)

Реализация тестового задания на позицию Backend Django Developer

Техническое задание:

![TT](hammerSystems/assets/TT.png)

# Реализация:

## /auth , начало верификации пользователя, ввод номера телефона

При первом входе пользователя в стадию верификации данные сохраняются в базу данных.
Формируется уникальный инвайт код (единожды), а так же устанавливается пароль в виде токена(каждый раз уникально-новый при авторизации)
После отправки номера телефона редирект на /auth/login

![start_ver](hammerSystems/assets/start_ver.png)

## /auth/login

Текущий токен пользователя указан на странице, ограничена возможность пользователю вводить неверные данные.

![token](hammerSystems/assets/token.png)

## /auth/profile

Профиль пользователя.
Вывод списка приглашенных пользователей, а так же формы для ввода чужой реферальной ссылки, а так же кнопка логаута.

![profile](hammerSystems/assets/profile.png)

## Добавление чужой реферальной ссылки:

Проверка ввода существующей реферальной ссылки, при отсутствии ссылки у всех пользователей выходит ошибка.

После добавления реально-существующей реферальной ссылки окно исчезает.

![after_enter](hammerSystems/assets/after_enter.png)

## Отображение списка добавленных пользователей:

После того, как кто-то воспользуется его ссылкой у него на странице будет данное отображение

![profile_first_user](hammerSystems/assets/profile_first_user.png)

*Добавить самого себя так же не получится.

## Установка

1. pip install -r requirements.txt (установка необходимых библиотек)

2. В файле hammerSystems/hammerSystems/setting.py указать данные локальной БД postgresql

3. cd hammerSystems

4. python manage.py migrate

5. python manage.py runserver
