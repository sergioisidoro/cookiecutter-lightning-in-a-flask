FROM python:3.9-alpine

RUN mkdir /code
WORKDIR /code

COPY bottle bottle/
COPY migrations migrations/

COPY Pipfile* ./

# INSTALL PIPENV AND OTHER DEPENDECIES
RUN pip install --no-cache-dir pipenv

# KEEP THIS SEPARATE COMMAND SO IT LEVERAGES DOCKER LAYER CACHE
RUN pipenv install --system --deploy --clear
