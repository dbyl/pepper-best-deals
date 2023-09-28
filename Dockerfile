FROM python:3.9
LABEL maintainer="dbyl.developer"

ENV PYTHONUNBUFFERED 1 \
    APP_DIR=/app

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./source /source
WORKDIR ${APP_DIR}
EXPOSE 8000

RUN apt-get update && apt-get install -y wget && \
    wget https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar && \
    mv selenium-server-standalone-3.141.59.jar /usr/local/bin && \
    apt-get clean

# Expose the port you want to use for Selenium (e.g., 4444)
EXPOSE 4444

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip3 install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

