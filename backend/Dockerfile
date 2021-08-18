FROM python:3.8-slim
WORKDIR /code
COPY requirements.txt /code
RUN pip install --upgrade pip && pip install -r /code/requirements.txt
COPY . /code
CMD python manage.py migrate
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000