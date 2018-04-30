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
    postgresql-contrib

# Install pip dependecies
RUN pip3 install --upgrade pip

# Insert Enviroment variable
ENV MODE_ENVIROMENT=production

# Create software folder and install requirements
ADD . /software
WORKDIR /software
RUN pip3 install -r requirements.txt

# Expose the port 8000
EXPOSE 8000

# Run the production script before and after any command
RUN chmod +x compose/production/prod.sh
ENTRYPOINT ["compose/production/prod.sh"]

# Run the server
CMD ["gunicorn", "--bind 0.0.0.0:8000", "tbl.wsgi"]
