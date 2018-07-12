# Update apt-get
apt-get update

# Install dependencies
apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  software-properties-common \
  nginx vim git \
  python3-dev \
  python3-pip \
  build-essential

# Modify language to PT-BR
locale-gen pt_BR.UTF-8

# Get the GPG docker key
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && apt-key fingerprint 0EBFCD88

# Get the repository of docker and docker-compose
curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

 # Install docker CE
apt-get update && apt-get install -y docker-ce

docker --version && docker-compose --version

# Clone the TBL repository
git clone https://github.com/VictorArnaud/TBL.git
cd TBL
pip3 install -f pgtbl/requirements.txt

# Run deploy enviroment
docker-compose -f ../docker-compose.deploy.yml up -d --build

# Config NGINX
# Copying the nginx configuration file into the container
cp scripts/nginx.conf /etc/nginx/conf.d/nginx.conf
# Removing the nginx default page
rm -rf /usr/share/nginx/html/*
rm -rf /etc/nginx/sites-enabled/* && rm -rf /etc/nginx/sites-available/*

# Pick up the static files and insert them inside the nginx repository so that they are served
python3 pgtbl/manage.py collectstatic --noinput
if [ -d "./pgtbl/tbl/staticfiles/" ]; then
  cp ./pgtbl/tbl/staticfiles/ /usr/share/nginx/html
fi
if [ -d "./pgtbl/tbl/mediafiles/" ]; then
  cp ./pgtbl/tbl/mediafiles/ /usr/share/nginx/html
fi

# Run nginx
service nginx start
systemctl status nginx.service
