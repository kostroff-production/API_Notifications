FROM python:3.8.10-alpine

ENV TZ Europe/Moscow
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add python3-dev \
                          gcc \
                          libc-dev \
                          libffi-dev \
                          postgresql-dev \
                          zlib libjpeg-turbo-dev libpng-dev \
                          freetype-dev lcms2-dev libwebp-dev \
                          harfbuzz-dev fribidi-dev tcl-dev tk-dev
                         

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install --no-cache-dir -r req.txt

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app

COPY ./entrypoint.sh .

COPY . /usr/src/app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
