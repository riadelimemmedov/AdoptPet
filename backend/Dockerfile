#?Pull official base image
FROM python:3.10-slim-buster

#?Set working directory
RUN mkdir /api
WORKDIR /api

#?Set environment variables
#Prevent Python from writing .pyc file
ENV PYTHONDONTWRITEBYTECODE 1
#Ensure python output is send directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

#?Install dependencies
COPY pyproject.toml /api
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

#?Copy project
COPY . /api

#?Application port
EXPOSE 8000

#?Run application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
