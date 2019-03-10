# Build an debian image
FROM python:3.6

# Update, Upgrade and configure locale
RUN apt-get update

# Install SO dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    build-essential

# Install pip dependecies
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ADD . /software
WORKDIR /software

# Insert Enviroment variable
ENV MODE_ENVIROMENT=development

# Run the dev script before and after any command
RUN chmod +x dockers/test/test.sh
ENTRYPOINT ["dockers/test/test.sh"]

# Expose 8080 port
EXPOSE 8080

# Run the server
CMD ["python3", "pgtbl/manage.py", "runserver", "0.0.0.0:8080"]