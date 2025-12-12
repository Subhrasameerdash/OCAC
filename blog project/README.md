# OCAC Blog

A production-ready blogging platform built with Django and Django REST Framework. The project delivers a Medium-style authoring experience with role-based access control, responsive Bootstrap UI, and a comprehensive REST API.

## Features

- User registration, login, and logout backed by Django auth
- Role-based permissions: authors manage their content, admins manage all posts
- Rich post model with title, Markdown content, optional hero image, timestamps, and author attribution
- SEO-friendly slugs and per-post detail pages (`/posts/<slug>/`)
- Homepage with pagination and search by title or author
- Personal dashboard listing the authenticated user's posts
- Image uploads stored under `media/` and served locally in development
- REST API exposed under `/api/posts/` with filtering, ordering, pagination, and permissions
- Django admin configured for full data management
- Whitenoise integration for efficient static file serving in production

## Tech Stack

- Python 3.13 + Django 5.2
- Django REST Framework
- Bootstrap 5 frontend
- SQLite (development) with optional PostgreSQL support via `psycopg2-binary`

## Getting Started

1. **Clone the repository**
   ```powershell
   git clone https://github.com/Subhrasameerdash/OCAC.git
   cd "OCAC/blog project"
   ```

2. **Create and activate a virtual environment**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the values (at minimum, set a secure `DJANGO_SECRET_KEY`)

5. **Apply database migrations**
   ```powershell
   python manage.py migrate
   ```

6. **Create a superuser account**
   ```powershell
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```powershell
   python manage.py runserver
   ```

8. **Access the site**
   - Frontend: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/
   - API root: http://127.0.0.1:8000/api/posts/

## Running Tests

Execute the Django test suite:
```powershell
python manage.py test
```

## API Overview

- `GET /api/posts/` — list posts (supports `search`, `ordering`, and pagination)
- `POST /api/posts/` — create a post (authenticated users only)
- `GET /api/posts/<id>/` — retrieve a post
- `PUT /api/posts/<id>/` — update a post (author or admin)
- `DELETE /api/posts/<id>/` — delete a post (author or admin)

Authentication uses session or basic auth. Admin users can manage any post; authors can only manage their own.

## Static & Media Files

- Static assets live in `static/` and are served via Whitenoise in production
- Uploaded images are stored in `media/`; ensure this directory is writable on the server

## Deployment Notes

- Set `DJANGO_DEBUG=False` and configure `DJANGO_ALLOWED_HOSTS`
- Run `python manage.py collectstatic` to gather static files
- Use a production-ready database (e.g., PostgreSQL) and configure credentials via environment variables

## License

This project is provided as-is for educational purposes. Adapt to your organization's licensing needs before deployment.
