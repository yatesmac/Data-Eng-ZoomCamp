FROM python:3.13-slim

WORKDIR /app

RUN apt update

RUN apt install wget

RUN pip install pandas sqlalchemy psycopg2

COPY load_data.py load_data.py

COPY args args

RUN python load_data.py -args

ENTRYPOINT ["bash"]