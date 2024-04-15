FROM python:3.10-slim

WORKDIR /

COPY ./requirements.txt ./req.txt

COPY . .

RUN pip3 install -r req.txt

ENV PYTHONPATH "/"

COPY start.sh /start.sh
RUN chmod +x start.sh

COPY alembic.ini /alembic.ini
COPY migrations /migrations
