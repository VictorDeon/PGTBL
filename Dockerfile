# Build an debian image
FROM debian:8.7

# Set the working directory to /software
ADD . /software
WORKDIR /software

# Update, Upgrade and configure locale
RUN apt-get update

# Install dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    gettext \
    build-essential

RUN pip3 install --upgrade pip
RUN pip3 install -r tbl/requirements.txt
