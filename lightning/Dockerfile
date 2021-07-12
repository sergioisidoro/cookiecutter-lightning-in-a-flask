FROM python:3.9-alpine

RUN mkdir /code
WORKDIR /code

RUN apk update --no-cache && \
    apk add --no-cache build-base postgresql-dev gcc python3-dev musl-dev

COPY bottle bottle/
COPY migrations migrations/

COPY Pipfile* ./

# INSTALL PIPENV AND OTHER DEPENDECIES
RUN pip install --no-cache-dir pipenv

# KEEP THIS SEPARATE COMMAND SO IT LEVERAGES DOCKER LAYER CACHE
RUN pipenv lock
RUN pipenv install --system --deploy --clear
