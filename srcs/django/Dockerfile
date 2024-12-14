FROM python:3.13.0-bookworm

COPY ./install.sh .
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

CMD ["bash", "./install.sh"]
