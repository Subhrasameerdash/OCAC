# Django E-commerce Platform

A production-ready e-commerce web application built with Django 5, Bootstrap 5, and SQLite. It supports user authentication, product browsing, cart management, and a simple checkout flow.

## Features
- User registration, login, and logout using Django's auth system.
- Product catalog with search and detail pages.
- Persistent cart per user with quantity updates and item removal.
- Checkout form collects shipping details and clears the cart on confirmation.
- Admin panel for managing products, users, and cart items.

## Project Structure
```
ecommerce_project/
├── manage.py
├── requirements.txt
├── README.md
├── ecommerce_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   ├── products/
│   └── cart/
├── templates/
└── static/
```

## Setup
```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Seed Data
Use the Django admin at `/admin/` to create categories and products. Sample steps:
1. Log in with the superuser you created.
2. Add products with images, prices, and stock levels.
3. Create test users or register directly from the site.

## Running Tests
No automated tests are included. Use manual testing to validate registration, login, cart operations, and checkout.

## Deployment Notes
- Replace SQLite with PostgreSQL or MySQL in `ecommerce_project/settings.py` for production.
- Configure static/media file hosting (e.g., AWS S3) and set up HTTPS.
- Update `ALLOWED_HOSTS` and security settings before deployment.
