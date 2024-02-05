FROM python:3.9

COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /code

COPY src/ /code

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]