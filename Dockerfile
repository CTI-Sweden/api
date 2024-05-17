FROM python:3.12-alpine
WORKDIR /app

RUN adduser -S api && \
    chown api /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

COPY . .

USER api
EXPOSE 8000/tcp
# ENTRYPOINT [ "cat", "/etc/shadow" ]
ENTRYPOINT [ "fastapi", "run" ]

