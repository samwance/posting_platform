# Paid content posting platform

### Description: 
A platform for publishing user-generated content. This project utilizes Django and PostgreSQL as the backend framework and database, respectively. User registration is based on phone numbers.
## Getting Started:

1) Clone the repository:
```
git clone https://github.com/samwance/posting_platform.git
```
2) Navigate to the project directory:
```
cd posting_platform
```
3) Create a .env file with the required environment variables. You can find a sample .env file in the project directory.

4) Run the Django migrations to set up the database:
```
python manage.py migrate
```
To create a superuser for the Django admin site:
```
python manage.py createsuperuser
```

Start the Django development server:
```
python manage.py runserver
```
Open your web browser and navigate to http://localhost:8000/admin/ to access the Django admin site.

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
