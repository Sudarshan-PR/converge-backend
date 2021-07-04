release: python manage.py migrate

web: gunicorn Converge.asgi:application -k uvicorn.workers.UvicornWorker