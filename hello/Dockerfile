# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWIRTEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /DjPro

# Install dependencies
COPY Pipfile Pipfile.lock /DjPro/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /DjPro/