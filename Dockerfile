FROM python:3.6.4-stretch

MAINTAINER Django <django@macetado.com>

ARG release=undefined
ENV RELEASE=$release

ENV DJANGO_COLORS="dark"

# Creating workspace
ENV WORKSPACE=/usr/src/app
RUN mkdir -p $WORKSPACE
WORKDIR $WORKSPACE

# Project dependency
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . $WORKSPACE

CMD ["./cmd.sh"]
