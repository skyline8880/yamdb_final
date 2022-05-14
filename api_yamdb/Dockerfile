FROM python:3.7-slim

WORKDIR /app

COPY /requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

# CMD python manage.py runserver 0:5000

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:5000" ]
