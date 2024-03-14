FROM python:3.9
LABEL maintainer="dbyl.developer"


RUN mkdir /app
ENV PYTHONUNBUFFERED 1 \
    APP_DIR=/app

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./source /source
WORKDIR ${APP_DIR}
EXPOSE 7000


ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip3 install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi
COPY . /app/



ENV PATH="/py/bin:$PATH"

