# BotForwarding_Django

## Описание

Настраиваемый парсер Telegram, с возможностью добавления любого количества открытых каналов для парсинга. Может работать в двух режимах:

   1. По умолчанию сохраняет посты в базу данных для дальнейшего редактирования. После подтверждения изменения отправляет пост в целевой канал.
   2. Пересылка постов напрямую в целевой канал, без сохранения в БД и возможности редактирования 

## Технологии

Django, DRF, Rest API, Pyrogram, PostgreSQL, django-signals, docker

## Как запустить

Создать .env файл в корне проекта вида:

```env
API_ID = <свой api_id>
API_HASH = <свой api_hash>
DEBUG = <True или False>
HOST = <свой хост, либо *>
SECRET_KEY = <свой secret key django>
DB_NAME = postgres
DB_USER = postgres
DB_PASS = postgres
DB_HOST = db
DB_PORT = 5432
```

Из корневой директории запустить docker-compose

```bash
docker-compose up -d
```

При первом запуске требуется создать сессию Pyrogram, так что идём в контейнер

```bash
docker exec -it combined_app bash
```

Переходим в директорию api/app и запускаем скрипт

```bash
cd api/app
python manage.py runscript create_session
```

И заодно создадим суперюзера
```bash
python manage.py createsuperuser
```

После создания сессии нужно перезапустить docker-compose

```bash
docker-compose down
docker-compose up
```

Админка будет доступна по адресу http://0.0.0.0:8000/admin.

Для работы приложения нужно добавить целевой канал(куда будут отправляться посты) и каналы для парсинга, с указанием добавленного целевого канала.

Для переключения режима работы в описании целевого канала есть флажок "*Парсинг прямо в канал*", активируйте его, если хотите сделать простую пересылку постов без сохранения в БД.

Также есть возможность выключить парсинг для целевого канала, для этого нужно снять флажок "*Включить парсинг*".

##  Скриншоты

*страница с пользователями*
![Снимок экрана от 2023-06-21 11-24-59](https://github.com/komediantto/BotForwarding_Django/assets/62796239/8bc45ddd-64c9-469c-921f-86e0ca32de76)

*страница с постами*
![Снимок экрана от 2023-06-21 11-27-17](https://github.com/komediantto/BotForwarding_Django/assets/62796239/4fd34724-041d-492f-9a45-8d043e1efb92)

*страница с целевыми каналами*
![Снимок экрана от 2023-06-21 11-27-48](https://github.com/komediantto/BotForwarding_Django/assets/62796239/f67ece05-00ff-4436-bceb-d62c2cdd1f02)

*страница с каналами для парсинга*
![Снимок экрана от 2023-06-21 11-28-13](https://github.com/komediantto/BotForwarding_Django/assets/62796239/b72bf5f5-4906-491a-9f52-00a24574b28a)

*страница с медиафайлами*
![Снимок экрана от 2023-06-21 11-28-49](https://github.com/komediantto/BotForwarding_Django/assets/62796239/a5b5f982-6da6-4aff-8d32-c821aea28f9a)

