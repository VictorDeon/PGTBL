Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.define :tbl do |web_config|
    config.vm.network "forwarded_port", guest: 80, host: 8000, host_ip: "192.168.45.21"
    # config.vm.provision "shell", path: "scripts/bootstrap.sh"
    config.vm.provision "shell", inline: <<-SHELL
      # Update apt-get
      apt-get update

      # Install dependencies
      apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common \
        nginx vim git

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

      # Run deploy enviroment
      docker-compose -f docker-compose.deploy.yml up -d --build
    SHELL
  end
end
