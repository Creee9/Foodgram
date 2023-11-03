# Foodgram - продуктовый помощник
https://foodgram101.hopto.org


![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)
![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)
![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)
![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)
![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)
![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)
![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)
![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)
![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)


Foodgram - приложение, где пользователи публикуют свои рецепты, могут
подписываться на публикации других авторов, а также добавлять их рецепты в избранное. 
В приложении реализована возможность составления списка покупок для ваших любимых рецептов! 


## Развертывание проекта через Docker

Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

Клонируйте репозиторий с проектом на свой компьютер.
```bash
git clone https://github.com/creee9/foodgram-project-react.git
```

Выполните команду сборки docker-compose:
```
docker-compose up -d --buld.
```

Выполните миграции:
```
docker-compose exec backend python manage.py migrate
```

Создайте суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```

Соберите файлы статики:
```
docker-compose exec backend python manage.py collectstatic
```
Заполните базу предоставленными данными:
```
docker-compose exec backend python manage.py add_ingredients_from_data
```
Для корректного создания рецепта, необходимо создать пару тегов в базе через админ-панель.



### Основные адреса: 
| Адрес                 | Описание |
|:----------------------|:---------|
| 127.0.0.1            | Главная страница |
| 127.0.0.1/admin/     | Для входа в панель администратора |
| 127.0.0.1/api/docs/  | Описание работы API |

##Адрес сервера
https://foodgram101.hopto.org/

## Автор:
Беликов Тимур<br>
belikov.t9@yandex.ru
