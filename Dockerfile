# Start with a Python image.
FROM python:3.8.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
RUN mkdir /code/static
WORKDIR /code

RUN apt-get update &&  apt-get install -y binutils libproj-dev gdal-bin

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install psycopg2-binary

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/


RUN python manage.py collectstatic --noinput
