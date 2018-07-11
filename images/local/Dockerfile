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
COPY pgtbl/requirements.txt /requirements/local.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements/local.txt

# Create a user
RUN useradd -m developer
ADD . /home/developer
WORKDIR /home/developer

# Insert Enviroment variable
ENV MODE_ENVIROMENT=development

# Run the dev script before and after any command
RUN chmod +x images/local/dev.sh
ENTRYPOINT ["images/local/dev.sh"]

# Expose 8000 port
EXPOSE 8000

# Set the container user
USER developer

# Run the server
CMD ["python3", "pgtbl/manage.py", "runserver", "0.0.0.0:8000"]
