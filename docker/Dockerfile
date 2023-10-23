FROM python:3.9

WORKDIR /code

COPY requirements.txt /code

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "server.py"]
