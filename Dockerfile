FROM python:3.9

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /backend/
RUN python3 -m pip install --upgrade pip  \
    && pip install wheel  \
    && pip install -r requirements.txt

COPY . /backend/
