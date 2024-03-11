# Use a multi-stage build
FROM python:3.10.13-alpine3.19 AS builder

LABEL maintainer="mdahtotul@gmail.com"

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# variables
ARG DEV=false
# Install build dependencies && create a non-root user
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

# Final production image
FROM python:3.10.13-alpine3.19
# Copy the virtual environment from the builder stage
COPY --from=builder /py /py
# Copy application code
COPY ./api /api
# Set working directory
WORKDIR /api
#Expose port
EXPOSE 8000
# Create a non-root user
RUN adduser \
      --disabled-password \
      --no-create-home \
      django-user

# Set PATH to include Python virtual environment
ENV PATH="/py/bin:$PATH"
# Set user and permissions
USER django-user