# Python image to use.
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update

# Update pip.
RUN python -m pip install --upgrade pip

# Copy the requirements file used for dependencies.
COPY requirements.txt .

# Install any needed packages specified in requirements.txt.
RUN pip install -r requirements.txt

# Copy the rest of the working directory contents into the container at /app.
COPY . .

# Add path to pythonpath.
ENV PYTHONPATH=/app/

# Run test when the container launches.
ENTRYPOINT ["pytest", "tests/test_data_loader.py"]