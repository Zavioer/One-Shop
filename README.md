# One-Shop
E-commerce platform created with python Django framework.

## Tech stack
- Django
- Bootstrap
- PostgreSQL

## Features
✅ Sing in/up

✅ Product CRUD

✅ Shopping cart

✅ Online payment (Przelewy24)

✅ Google OAuth

✅ Email verification

❌ Anonymous session

❌ Choose shipping method


## Instalation
Python version `3.8.10` 

1. Create `.env` file in `shop/`
2. Fill variables in created file
    - `DJANGO_SECRET_KEY`
    - `DJANGO_DEBUG`
    - `DJANGO_ALLOWED_HOSTS`
    - `DB_NAME`
    - `DB_USER`
    - `DB_PASSWORD`
    - `DB_HOST`
    - `DB_PORT`
    - `GOOGLE_CLIENT_ID`
    - `GOOGLE_CLIENT_SECRET`
    - `EMAIL_HOST`
    - `EMAIL_USER`
    - `EMAIL_PASSWORD`
    - `EMAIL_PORT`
3. Install required packages `pip install -r requirements.txt`
4. Create database tables `python manage.py migrate`
5. Run app development server `python manage.py runserver`

## Licence
MIT
