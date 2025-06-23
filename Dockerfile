# Python image to use.
FROM python:3.10-slim-buster

RUN apt-get update

# Update pip
RUN python -m pip install --upgrade pip

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt