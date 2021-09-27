FROM python:3
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --no-input
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]