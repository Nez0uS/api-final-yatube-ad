# API для Yatube

## Описание
REST API для социальной сети Yatube. Позволяет создавать посты, комментарии, подписываться на авторов.

## Технологии
- Django 3.2
- Django REST Framework 3.12
- JWT-аутентификация (Djoser)
- SQLite

## Установка

```bash
git clone https://github.com/Nez0uS/api-final-yatube-ad.git
cd api-final-yatube-ad
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd yatube_api
python manage.py migrate
python manage.py runserver
