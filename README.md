# SHARE WITH ME
##  BACKEND: Платформа для онлайн-бронирования услуг психологов и психотерапевтов

### Описание
Бэкенд веб-сервиса для поиска веб-сервиса "Платформа для онлайн-бронирования услуг психологов и психотерапевтов". Возможности:
 - TBD;
 - TBD;
### Инструменты:
![image](https://img.shields.io/badge/Python%203.9-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django%204.1-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest%203.14-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![image](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

### Развертывание бэкенда на время разработки
Склонировать репозиторий:
```
git clone git@github.com:services-psychologists-psychotherapists/backend.git
```
Открыть папку с проектом:
```
cd backend
```
Во время разработки основная рабочая часть кода находится в ветке develop, она сливается с веткой main по необходимости. Для доступа к актуальной версии кода и документации:
```
git checkout develop
```
Если Вы ранее копировали проект и с тех пор команда делала коммиты, надо загрузить изменения:
```
git pull
```
Создать виртуальное окружение, активировать его и обновить менеджер пакетов pip и установить зависимости проекта:
```
Windows:py -m venv venv     /   Linux & MacOS: python3 -m venv venv
Windows:source venv/scripts/activate     /   Linux & MacOS: source venv/bin/activate
Windows:python -m pip install --upgrade pip     /   Linux & MacOS: python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Пример содержания .env файла (для проверки документации не требуется):
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY='16dg2dj1jfu+mc+ylzojdiw_fk!f#x*8ci!u2-asdadnkqlkwdk'
EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend'
EMAIL_HOST_USER='share.with.me-help@yandex.ru'
EMAIL_HOST_PASSWORD='emailpassword'
EMAIL_HOST='smtp.someserver.ru'
EMAIL_PORT=587
ZOOM_CLIENT_ID='zoomclientid'
ZOOM_ACCOUNT_ID='zoomaccountid'
ZOOM_CLIENT_SECRET='zoomclientsecret'
```
Запуск сервера:
```
python manage.py runserver
```
Документация доступна по адресу:
```
http://127.0.0.1:8000/swagger/
```
