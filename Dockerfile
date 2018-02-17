# Build an debian image
FROM debian:8.7

# Export 8000 port
EXPOSE 8000

# Set the working directory to /software
ADD . /software
WORKDIR /software

# Update, Upgrade and configure locale
RUN apt-get update

# Install SO dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    gettext \
    vim \
    build-essential

# Set the secret_key to enviroment
ENV MODE_ENVIROMENT='development'

# Install pip dependecies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Execute django commands
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py compilemessages

# Execute the server (trade to deploy server)
CMD python3 manage.py runserver 0.0.0.0:8000
