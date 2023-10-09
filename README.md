# SHARE WITH ME
https://sharewithme.acceleratorpracticum.ru/

##  BACKEND: Платформа для онлайн-бронирования услуг психологов и психотерапевтов

### Инструменты:
![image](https://img.shields.io/badge/Python%203.9-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django%204.1-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest%203.14-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![image](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

### Описание
Бэкенд веб-сервиса для поиска веб-сервиса "Платформа для онлайн-бронирования услуг психологов и психотерапевтов". Возможности:
Все пользователи:
 - Аутентификация (JWT);
 - Поиск в каталоге с фильтрами (опыт, пол, возраст, темы, методы работы);
 - Просмотр страницы психолога, выбор свободных окон для записи;

Клиенты:
 - Личный кабинет с возможностью изменить данные в профиле;
 - Информация о ближайшей сессии и психологе пользователя (с которым прошла последняя сессия);
 - Запись на сессию и отмена записи (из ЛК);

Психологи:
 - Личный кабинет: изменение данных профиля + работа с рабочим календарем через создание/удаление окон записи; 

Нестандартные фичи:
 - Отдельная регистрация для клиентов и психологов; 
 - Верификация психологов через админ-панель (активация с автоматической рассылкой);
 - Организация видео-чата с использованием API Zoom. 

### API-документация:
```
https://sharewithme.acceleratorpracticum.ru/swagger/
```

### Пример содержания .env файла:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY='16dg2dj1jfu+mc+ylzojdiw_fk!f#x*8ci!u2-asdadnkqlkwdk'
DEBUG=False
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=*
EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend'
EMAIL_HOST_USER='share.with.me-help@yandex.ru'
EMAIL_HOST_PASSWORD='emailpassword'
EMAIL_HOST='smtp.someserver.ru'
EMAIL_PORT=587
ZOOM_CLIENT_ID='zoomclientid'
ZOOM_ACCOUNT_ID='zoomaccountid'
ZOOM_CLIENT_SECRET='zoomclientsecret'
```

### Запуск проекта
Склонировать репозиторий:
```
git clone git@github.com:services-psychologists-psychotherapists/backend.git
```
Открыть папку с проектом:
```
cd backend
```
Запуск контейнеров:
```
docker-compose up -d --build
docker-compose exec -it psy_backend python collectstatic --noinput
docker-compose exec -it psy_backend python manage.py migrate
```
Наполнение базы фикстурами:
```
docker-compose exec -it psy_backend python manage.py loaddata fixtures.json 
```