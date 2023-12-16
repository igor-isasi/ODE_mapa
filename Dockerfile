FROM python:3.9

WORKDIR /code

COPY ./ /code

RUN pip3 install -r requirements.txt

RUN ls -l /code/*

EXPOSE 5000

CMD ["python3", "server.py"]