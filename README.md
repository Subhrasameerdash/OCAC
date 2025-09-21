# OCAC Projects Repository

This repository contains three Django-based web applications: Portfolio Project, Task Management System, and Weather Forecasting App.

## 📂 Repository Structure

```
OCAC/
├── Portfolio project/        # Personal portfolio website
├── Task management Project/ # Task management application
└── weather forecasting app/ # Weather forecasting application
```

## 🚀 Projects Overview

### 1. Portfolio Project

A personal portfolio website built with Django to showcase projects, skills, and experience.

**Features:**

- Responsive design
- Project showcase
- Contact form
- About me section
- Resume download option

**Tech Stack:**

- Django 5.2.6
- HTML/CSS
- Bootstrap
- SQLite3

### 2. Task Management Project

A full-featured task management system with user authentication.

**Features:**

- User registration and authentication
- Create, Read, Update, Delete (CRUD) operations for tasks
- Task status tracking
- User-specific task lists
- Responsive UI

**Tech Stack:**

- Django 5.2.6
- HTML/CSS/JavaScript
- SQLite3
- Bootstrap

### 3. Weather Forecasting App

A weather application that provides current weather information for any city.

**Features:**

- Real-time weather data
- City-based weather search
- Temperature display
- Weather condition descriptions
- Weather icons
- High-resolution city images

**Tech Stack:**

- Django 5.2.6
- OpenWeatherMap API
- Google Custom Search API
- HTML/CSS
- Bootstrap
- JavaScript

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.13+
- pip (Python package manager)
- Git

### General Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/Subhrasameerdash/OCAC.git
cd OCAC
```

2. For each project, follow these steps:

```bash
cd <project-folder>
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Project-Specific Setup

#### Portfolio Project

```bash
cd "Portfolio project/portfolio"
python manage.py collectstatic
python manage.py runserver
```

#### Task Management Project

```bash
cd "Task management Project/todo"
python manage.py runserver
```

#### Weather Forecasting App

1. Set up environment variables:

   - Create a `.env` file in the project root
   - Add your API keys:
     ```
     OPENWEATHERMAP_API_KEY=your_api_key
     GOOGLE_SEARCH_API_KEY=your_google_api_key
     GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
     ```

2. Run the server:

```bash
cd "weather forecasting app/weatherproject"
python manage.py runserver
```

## 🌟 Features

### Portfolio Project

- Responsive design for all devices
- Project showcase with descriptions and images
- Contact form with email integration
- Resume download functionality
- Clean and modern UI

### Task Management Project

- Secure user authentication
- Task creation and management
- Task status updates
- User-specific task lists
- Intuitive user interface

### Weather Forecasting App

- Current weather conditions
- Temperature in Celsius
- Weather descriptions
- City-based weather search
- High-quality city images
- Error handling for invalid cities

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Subhra Sameer Dash**

## 🙏 Acknowledgments

- OpenWeatherMap API for weather data
- Google Custom Search API for city images
- Django community for the excellent framework
- Bootstrap team for the responsive UI components
