FROM python:3.8-alpine
MAINTAINER Kavian AmirMozafari

ENV PYTHONUNBUFFERED 1

COPY ./requirments.txt /requirments.txt
RUN apk add --update --no-cache postgresql-client postgresql-dev gcc libc-dev linux-headers
RUN pip install -r /requirments.txt

RUN mkdir /app
COPY ./app /app
WORKDIR /app

# create non-login (sys-user) user
RUN adduser -D user
# switch to user User because the user is root and it's dangrous
USER user