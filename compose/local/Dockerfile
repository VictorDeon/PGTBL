# Build an debian image
FROM python:3.6

# Update, Upgrade and configure locale
RUN apt-get update

# Install SO dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    gettext \
    vim \
    build-essential

# Install pip dependecies
COPY requirements.txt /requirements/local.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /software
