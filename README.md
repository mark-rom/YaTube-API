## YaTube API ##
### Описание: ###
YaTube является аналогом LiveJournal и позволяет создавать пубикации,делиться ими в сообществах, подписываться на других пользователей и комментировать их публикации. Неавторизованные пользователи могут только читать публикации.

YaTube реализован на `Djangorestframework 3.12.4`. Аутентификация на основе `Simple JWT`. Также в YaTube доступна пагинация запросов.

## Как запустить проект: ##

### Клонируйте репозиторий: ###

    git clone https://github.com/mark-rom/api_final_yatube.git

### Перейдите в репозиторий в командной строке: ###
    cd api_final_yatube

### Создайте и активируйте виртуальное окружение: ###
    python3.9 -m venv env

###### для Mac OS
    source env/bin/activate

###### для Windows OS
    source venv/Scripts/activate

### Установите зависимости из файла requirements.txt: ###
### Обновите pip:
    python3 -m pip install --upgrade pip

### Установите зависимости:
    pip install -r requirements.txt
  
### Выполните миграции: ###
    python3 manage.py migrate

### Запустить проект: ###
    python3 manage.py runserver

## Авторизация пользователей ##
  
1. Пользователь отправляет POST-запрос с параметрами `username` и `password` на эндпоинт `api/v1/jwt/create/` и получает JWT-токены `refresh` и `access`.
2. Обновить `access` токен возможно в течение 24 часов, направив POST-запрос с `refresh` токеном на эндпоинт `api/v1/jwt/refresh/`. В ответ придет новый `access` токен.
