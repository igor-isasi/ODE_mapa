FROM python:3.9

COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /code

COPY src/ /code

EXPOSE 5000

CMD ["python3", "run.py"]