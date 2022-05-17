FROM python:3.7-slim

ADD file:8b1e79f91081eb527b455431af58e823d8b84d9d0c8e5c47cb7bda7507954ae4 in / 

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:5000" ]
