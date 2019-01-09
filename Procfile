web: gunicorn manage:run
release: python manage.py db migrate && python manage.py db upgrade