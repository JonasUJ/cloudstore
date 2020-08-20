# pull official base image
FROM python:3.8-slim

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN apt-get update \
    && apt-get install -y postgresql gcc python3-dev musl-dev netcat git

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create directories
RUN mkdir ./logs && \
    mkdir ../files

# set environment variables
ENV PYTHONUNBUFFERED 1

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]