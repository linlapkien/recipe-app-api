FROM python:3.9-alpine3.13
LABEL maintainer="linlapkien.com"

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Build Arg DEV, set defaults value to false
# When run docker-compose.yml file, it will overwrite ARE DEV=true
ARG DEV=false

# RUN command when build image
# This create new virtual environment work with docker
RUN python -m venv /py && \
    # upgrade python package manager inside venv
    /py/bin/pip install --upgrade pip && \
    # install postgresql-client. package that we need install inside image
    apk add --update --no-cache postgresql-client jpeg-dev && \
    # virtual action, group installed packages into tmp-build-deps
    apk add --update --no-cache --virtual .tmp-build-deps \
        # This is list of packages that we need to install
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    # Install list of requirements inside docker image
    /py/bin/pip install -r /tmp/requirements.txt && \

    #When docker file run, it will install requirements.txt first, then dev=true, install more requirements.dev.txt to docker images.
    #if dev=true, install dev dependecies otherwise, not
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    # if u use if statement, u have to end like this:
    fi && \
    # remove tmp directory, we dont need any dependency when we created
    rm -rf /tmp && \
    # rm tmp-build-deps, we've install list of package above, then we will rm later on. This keep our dockerfile low weight.
    apk del .tmp-build-deps && \
    # add new user inside image.
    #Important !!! Dont run ur application using the root user!
    adduser \
        --disabled-password \
        --no-create-home \
        # Call the name of user: Django-user
        django-user && \
    # create directory for media and static files
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    # change owner of directory to django-user
    chown -R django-user:django-user /vol && \
    # change permission of directory to 755
    chmod -R 755 /vol

# update PATH ENV var
ENV PATH="/py/bin:$PATH"

USER django-user