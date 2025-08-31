# Job API

A RESTful API built with Django REST Framework for managing jobs, categories, companies, reviews, applications, authentication, and favorites.

## Features

- CRUD operations for jobs, categories, and companies.
- Filtering and searching for jobs.
- User authentication (signup, login, JWT token-based).
- Job applications management.
- Job and company reviews management.
- Favorite jobs for users.
- Pagination for job listings.
- JSON responses for easy integration with frontend applications.

## Requirements

- Python 3.8 or higher
- Django 3.2 or higher
- Django REST Framework
- djangorestframework-simplejwt (for authentication)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/zakariyae1889/Job-API.git


cd Job-API

python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows

pip install -r requirements.txt


python manage.py migrate
