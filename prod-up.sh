cd eatthis
gunicorn eatthisadmin.wsgi:application --bind 0.0.0.0:8000