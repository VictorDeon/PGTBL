## Stage 01: Getting static files ##
####################################

# Get the debian image with python3 installed
# Causes the image to be temporary and stored
# in the variable builder
FROM python:3.6 as builder

# Installs the S.O units
RUN apt-get update && apt-get install -y python3-dev python3-pip

# Install pip and project dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Insert the software into the container software folder
ADD . /software
WORKDIR /software

# Get static files
RUN python3 pgtbl/manage.py collectstatic --noinput

#################################################
## Stage 02: Configure nginx to service them ##
#################################################

# Get the image of nginx
FROM nginx:latest

# Removing nginx default configuration file
RUN rm -rf /etc/nginx/conf.d/*

# Copy nginx.conf to the nginx folder
COPY ./dockers/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Removing nginx default page
RUN rm -rf /usr/share/nginx/html/*

# Get the static files generated in the builder and store them in nginx
COPY --from=builder /software/pgtbl/tbl/staticfiles /usr/share/nginx/html

# Releases port 80
EXPOSE 80

# Run the nginx server
CMD ["nginx", "-g", "daemon off;"]