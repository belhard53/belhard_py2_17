FROM python

# set a directory for the app
WORKDIR /app

# copy all the files to the container
COPY . /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# tell the port number the container should expose
EXPOSE 5555

# run the command
CMD ["python", "./app/main.py"]


#docker push