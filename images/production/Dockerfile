# Build an debian image
FROM python:3.6

# Install SO dependecies
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libpq-dev \
    python3-setuptools \
    gettext \
    vim \
    build-essential \
    postgresql \
    nginx \
    postgresql-contrib && pip3 install --upgrade pip

# Create software folder and install requirements
ADD . /software
WORKDIR /software
RUN pip3 install -r requirements/requirements-prod.txt

# Insert Enviroment variable
ENV MODE_ENVIROMENT=production

# Expose the port 80
EXPOSE 8000

# Run the production script before and after any command
RUN chmod +x images/production/prod.sh
ENTRYPOINT ["images/production/prod.sh"]

CMD ["gunicorn", "--bind 0.0.0.0:8000", "--chdir pgtbl", "tbl.wsgi"]
