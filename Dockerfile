FROM python:3.8-alpine
MAINTAINER Kavian AmirMozafari

ENV PYTHONUNBUFFERED 1

COPY ./requirments.txt /requirments.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirments.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
COPY ./app /app
WORKDIR /app

RUN mkdir -p /vol/web/media /vol/web/static
# create non-login (sys-user) user
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
# switch to user User because the user is root and it's dangrous
USER user