FROM python:3.9-alpine3.13
LABEL maintainer="linlapkien.com"

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# RUN command when build image
# This create new virtual environment work with docker
RUN python -m venv /py && \ 
    # upgrade python package manager inside venv
    /py/bin/pip install --upgrade pip && \ 
    # Install list of requirements inside docker image
    /py/bin/pip install -r /tmp/requirements.txt && \
    # remove tmp directory, we dont need any dependency when we created
    rm -rf /tmp && \
    # add new user inside image.
    #Important !!! Dont run ur application using the root user!
    adduser \
        --disabled-password \
        --no-create-home \
        # Call the name of user: Django-user
        django-user

# update PATH ENV var
ENV PATH="/py/bin:$PATH"

USER django-user