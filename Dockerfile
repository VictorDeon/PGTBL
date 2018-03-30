# Build an debian image
FROM python:3.6

# Melhora a acessibilidade ao container
ENV PYTHONUNBUFFERED 1

# Set the working directory to /software
RUN mkdir /software
WORKDIR /software
ADD . /software

# Update, Upgrade and configure locale
RUN apt-get update

# Install SO dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    gettext \
    vim \
    build-essential \
    postgresql \
    postgresql-contrib

# Install pip dependecies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
