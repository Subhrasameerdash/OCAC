# OCAC Multi-Project Django Suite

This repository is a monorepo that bundles five independent Django applications that showcase different aspects of full-stack development: an e-commerce platform, a blogging platform with a REST API, a personal portfolio site, a task management system, and a weather dashboard. Each project lives in its own folder with its own virtual environment and `requirements.txt` file so you can run them independently or side-by-side.

## 📚 Projects at a Glance

| #   | Project                  | Path                                      | Highlights                                          | Primary Stack                                          |
| --- | ------------------------ | ----------------------------------------- | --------------------------------------------------- | ------------------------------------------------------ |
| 1   | E-commerce Platform      | `ecommerce_project/`                      | Product catalog, carts, checkout, admin workflows   | Django 5.2.7, Bootstrap, SQLite, Pillow                |
| 2   | Blog Platform + REST API | `blog project/`                           | Authoring UI, DRF endpoints, role-based permissions | Django 5.2, Django REST Framework, Bootstrap           |
| 3   | Portfolio Site           | `Portfolio project/`                      | Landing page + contact form                         | Django 5.2.6                                           |
| 4   | Task Management App      | `Task management Project/todo/`           | Authenticated TODO list with CRUD UI                | Django 5.2.6                                           |
| 5   | Weather Dashboard        | `weather forecasting app/weatherproject/` | Real-time weather + hero imagery                    | Django 5.2.6, OpenWeatherMap API, Google Custom Search |

## 🗂️ Repository Layout

```
OCAC/
├── blog project/
├── ecommerce_project/
├── Portfolio project/
├── Task management Project/
└── weather forecasting app/
```

Each project root contains its own `manage.py`, `requirements.txt`, static and template assets, and (optionally) a local virtual environment directory. Feel free to delete and recreate those virtual environments if you prefer a different layout.

## ⚙️ Prerequisites

- Python 3.13+
- pip (ships with Python)
- Git
- Recommended: virtualenv or `python -m venv`

## 🚀 Quick Start

1. **Clone the repository**
   ```powershell
   git clone https://github.com/Subhrasameerdash/OCAC.git
   cd OCAC
   ```
2. **Pick a project folder** (see table above).
3. **Create & activate a virtual environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. **Install dependencies + apply migrations**
   ```powershell
   pip install -r requirements.txt
   python manage.py migrate
   ```
5. **Run the development server**
   ```powershell
   python manage.py runserver
   ```

Repeat steps 2–5 for any other project you want to explore. Each project can run simultaneously on a different port (set via `python manage.py runserver 0.0.0.0:8001`, etc.).

> 💡 Tip: Keep environment-specific secrets (API keys, database URLs, etc.) in a `.env` file or Windows environment variables rather than committing them to source control.

## 🧭 Project Guides

### 1. E-commerce Platform (`ecommerce_project/`)

A production-ready storefront featuring authentication, a product catalog, cart persistence, and a simple checkout pipeline.

**Features**

- User registration/login/logout via Django auth
- Product catalog with detail pages, pricing, and stock tracking
- Persistent carts per user with quantity updates and removal
- Checkout form collects shipping details and clears the cart on success
- Order history stored in the database for auditing
- Django admin configured for products, orders, and users

**Tech Stack**: Django 5.2.7, Bootstrap 5, SQLite (dev), Pillow for media uploads

**Run locally**

```powershell
cd "ecommerce_project"
python -m venv env
env\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Key URLs**

- Storefront: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

> 📦 Seed data: use the admin to add categories, products (with images), and test users. The cart and order models live in `apps/cart/` and `apps/products/`.

### 2. Blog Platform + REST API (`blog project/`)

A Medium-style blogging experience with Bootstrap pages, custom template tags, and a DRF-powered API for posts.

**Features**

- User registration/login/logout using Django auth
- CRUD UI for posts (list, detail, create, edit, delete)
- Author dashboard (`/my-posts/`) with per-user filtering
- Image uploads stored under `media/posts/`
- REST API exposed under `/api/posts/` with search, ordering, filtering, and pagination
- Role-based permissions: authors manage their own posts; staff manage everything

**Tech Stack**: Django 5.2, Django REST Framework, Bootstrap 5, SQLite (dev)

**Run locally**

```powershell
cd "blog project"
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Optional: copy .env.example to .env and set DJANGO_SECRET_KEY, DEBUG, etc.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**API Base Path & Permissions**

- All endpoints live under `/api/` per `config/urls.py`.
- The DRF router registers posts at `/api/posts/` (`blog/api_urls.py`).
- `IsAuthenticatedOrReadOnly`: anonymous users can read; writes require login.
- `IsAuthorOrAdmin`: only the author or staff can update/delete (`blog/permissions.py`).

**Endpoints**

| Method    | Endpoint           | Notes                                                               |
| --------- | ------------------ | ------------------------------------------------------------------- |
| GET       | `/api/posts/`      | List posts; supports `?search=`, `?ordering=`, `?author__username=` |
| POST      | `/api/posts/`      | Create post; authenticated users only                               |
| GET       | `/api/posts/<id>/` | Retrieve single post                                                |
| PUT/PATCH | `/api/posts/<id>/` | Update post (author/admin)                                          |
| DELETE    | `/api/posts/<id>/` | Delete post (author/admin)                                          |

**Testing**

```powershell
python manage.py test
```

### 3. Portfolio Site (`Portfolio project/`)

A lightweight personal website with a landing page and contact form.

**Features**

- Home/landing page (`portfolioapp/index.html`)
- Contact page (`/contact/`) that posts into the `Contact` model
- Static assets in `static/` (CSS, images, resume PDFs)

**Run locally**

```powershell
cd "Portfolio project/portfolio"
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r ../requirements.txt  # if present, otherwise install Django manually
python manage.py migrate
python manage.py runserver
```

> ✉️ Captured contact submissions reside in the `Contact` model defined in `portfolioapp/models.py`. Wire up email sending or admin moderation as needed.

### 4. Task Management App (`Task management Project/todo/`)

A simple TODO tracker with signup/login, per-user task lists, and CRUD actions.

**Features**

- Custom signup/login/logout views backed by Django auth
- Auth-protected todo list (`/todopage/`) with task creation
- Edit (`/edit_todo/<id>/`) and delete (`/delete_todo/<id>/`) actions with ownership checks
- Flash messaging for validation feedback (empty titles, duplicate usernames, etc.)

**Run locally**

```powershell
cd "Task management Project/todo"
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt  # create if missing; minimum Django dependency
python manage.py migrate
python manage.py runserver
```

**Key URLs**

- `/signup/` — create account
- `/loginn/` — authenticate
- `/todopage/` — list & add tasks (requires login)
- `/signout/` — logout

### 5. Weather Dashboard (`weather forecasting app/weatherproject/`)

A single-page view that fetches live weather data and a matching city image.

**Features**

- Search for any city (defaults to “goa”)
- Weather readings via OpenWeatherMap (temperature, description, icon)
- City hero imagery fetched using Google Custom Search API
- Friendly error handling when APIs fail or a city is not found

**Environment Variables**

Update the view (`weatherapp/views.py`) to load secrets from environment variables instead of hard-coding:

```
OPENWEATHERMAP_API_KEY=<your_key>
GOOGLE_SEARCH_API_KEY=<your_key>
GOOGLE_SEARCH_ENGINE_ID=<engine_id>
```

**Run locally**

```powershell
cd "weather forecasting app/weatherproject"
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt  # install Django + requests
python manage.py runserver
```

## 🧪 Testing

- **Blog project**: `python manage.py test`
- **Other projects**: manual QA (no automated suites yet). Consider adding Django tests under each app’s `tests.py` before shipping to production.

## 🧰 Tooling & Tips

- **Virtual environments**: Each project already includes a sample venv folder. Delete/recreate if your OS blocks execution (e.g., policy on downloaded scripts).
- **Static & media files**: For e-commerce and blog projects, run `python manage.py collectstatic` before deploying. Ensure `media/` is writable when handling uploads.
- **Ports**: Default Django port is 8000; use `python manage.py runserver 8001` (etc.) when running multiple apps simultaneously.
- **Database**: SQLite is ideal for demos; switch to PostgreSQL or MySQL for production by editing each project’s `settings.py`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/awesome`
3. Commit your changes: `git commit -m "Add awesome"`
4. Push: `git push origin feature/awesome`
5. Open a pull request describing the changes per project folder

## 📝 License

This repository is licensed under the MIT License. See [`LICENSE`](LICENSE) for full text.

## 👤 Author

**Subhra Sameer Dash** — Reach out on GitHub for collaboration or questions.
