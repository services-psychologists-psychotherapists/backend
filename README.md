# SHARE WITH ME
https://sharewithme.site/

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
https://sharewithme.site/swagger/
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
docker-compose exec -it psy_backend python manage.py loaddata static/fixtures/fixtures.json
docker-compose exec -it psy_backend python manage.py loaddata static/fixtures/users.json
docker-compose exec -it psy_backend python manage.py loaddata static/fixtures/psycho.json 
```
Образец файла .env лежит в репозитории.

### Разработчики:
 - [Вера Фадеева](https://github.com/verafadeeva): Psychologists app + API
 - [Руслан Атаров](https://github.com/ratarov): Clients app + API, Sessions app + API, mail service
 - [Владислав Нестеров](https://github.com/nevladi): Users app + API, CI/CD workflows