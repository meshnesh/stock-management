web: gunicorn manage:runserver
release: python manage.py db migrate && python manage.py db upgrade