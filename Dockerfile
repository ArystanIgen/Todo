FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /todo_service

# Set the working directory to /music_service
WORKDIR /todo_service

# Copy the current directory contents into the container at /music_service
ADD . /todo_service/

# Install any needed packages specified in requirements.txt
ADD requirements.txt /todo_service/requirements.txt
RUN pip install -r /todo_service/requirements.txt


CMD ["/todo_service/start.sh"]