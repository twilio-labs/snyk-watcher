FROM python:3.9.0-alpine

ENV APP_USER snyk_watcher
ENV APP_DIR /home/$APP_USER
WORKDIR $APP_DIR

# Create user and group
RUN addgroup -S $APP_USER && \
    adduser	 -S -G $APP_USER -s /sbin/nologin $APP_USER

RUN apk update

COPY requirements.txt $APP_DIR/requirements.txt
RUN apk add --virtual build-dependencies python3-dev build-base \
	&& pip3 install --upgrade pip \
	&& pip3 install -r $APP_DIR/requirements.txt \
	&& rm -rf /var/cache/apk/* \
	&& apk del build-dependencies

COPY app $APP_DIR/app
COPY bin $APP_DIR/bin

EXPOSE 8000

USER $APP_USER

CMD (gunicorn app.main:app -b 0.0.0.0:8000 -w 3 -k uvicorn.workers.UvicornWorker)
