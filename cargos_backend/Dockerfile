# pull official base image
FROM python:3.6-alpine

# set work directory
WORKDIR /usr/src/cargos_backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/cargos_backend/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/cargos_backend/entrypoint.sh

# copy project
COPY . /usr/src/cargos_backend/

EXPOSE 8000
# run entrypoint.sh
ENTRYPOINT ["/usr/src/cargos_backend/entrypoint.sh"]