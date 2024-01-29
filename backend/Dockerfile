#?Pull official base image
FROM python:3.11.4-slim-buster


#?Set working directory
RUN mkdir /backend
WORKDIR /backend


#?Set environment variables
#Prevent Python from writing .pyc file
# ENV PYTHONDONTWRITEBYTECODE 1 
#Ensure python output is send directly to the terminal without buffering
# ENV PYTHONUNBUFFERED 1



#?Install dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt /usr/src/app/requirements.txt
# RUN pip install -r requirements.txt


#?Install Netcat
# RUN apt-get update && apt-get install -y netcat


#?Copy entrypoint.sh
# COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
# RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
# RUN chmod +x /usr/src/app/entrypoint.sh


# ENTRYPOINT ["./entrypoint.sh"]

#?Copy project
# COPY . /usr/src/app/


#?Application port
# EXPOSE 8000


#?Run script on cmd terminal
# CMD ["gunicorn","--chdir","backend","--bind",":8000","config.wsgi:application","--reload"]



#?Run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
