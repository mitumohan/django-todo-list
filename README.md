# Django To-Do List

A to-do list web app built with Django. You can add, edit, complete and delete tasks, and give each one a priority and a due date.

## Built with

- Python
- Django
- HTML templates

## Run it on your computer

1. Clone the repo and go into it:
   ```bash
   git clone https://github.com/mitumohan/django-todo-list.git
   cd django-todo-list
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your private settings file and give it a secret key:
   ```bash
   cp .env.example .env
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Paste the generated key into `.env` as the value of `DJANGO_SECRET_KEY`.
5. Set up the database and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
6. Open http://127.0.0.1:8000 in your browser.

## Run the tests

```bash
python manage.py test
```

## Project structure

```
tasks/          # the to-do app: models, views, forms, templates, tests
todoproject/    # Django project settings and URLs
manage.py       # Django's command-line helper
.env.example    # template for your private .env file
```
