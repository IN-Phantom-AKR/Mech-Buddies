release: python manage.py migrate && python manage.py seed_services
web: gunicorn Roadside_Assistance.wsgi:application