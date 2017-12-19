FROM python:3
ENV PYTHONBUFFERED 1
ENV GOSU_VERSION 1.10

RUN apt-get update \
    && apt-get install -y curl gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Install gosu so we can create a non-root user
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
    && curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture).asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu

# Setup an entrypoint script to create the non-root user
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# App setup
RUN mkdir /app 
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
