# Get the debian image with python3 installed
FROM python:3.6
# Evitar delay no log do django
ENV PYTHONUNBUFFERED 1

# Installs the S.O units
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libpq-dev \
    gettext \
    vim \
    build-essential

# Install pip and project dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Inserts the software into the container software folder and creates a user
ADD . /home/pgtbl
WORKDIR /home/pgtbl

# Inserts production environment variable
ENV MODE_ENVIROMENT=production

# Releases the 8000 port
EXPOSE 8000

# Run the server before and after each command in the container
RUN chmod +x dockers/production/prod.sh
ENTRYPOINT ["dockers/production/prod.sh"]

# Run the production server
CMD ["gunicorn", "--bind 0.0.0.0:8000", "--chdir pgtbl", "tbl.wsgi", "--reload --graceful-timeout=900 --timeout=900 --log-level DEBUG --workers 5"]
