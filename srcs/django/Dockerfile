FROM python:3.13.0-bookworm

COPY ./install.sh .
RUN pip install django psycopg

CMD ["bash", "./install.sh"]
