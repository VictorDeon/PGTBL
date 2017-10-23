# DEVELOPMENT ENVIRONMENT
# The last version of vagrant configuration
Vagrant.configure("2") do |config|

  # Configure the image of virtualbox ubuntu 16.04 64-bits
  config.vm.box = "ubuntu/xenial64"

  # Create machine call tbl
  config.vm.define :tbl do |web_config|

    # Create a private network IP
    config.vm.network "private_network", ip: "192.168.33.10"

    # Mapping ports from vagrant 8080 to localhost 8080
    config.vm.network :forwarded_port, host_ip: "127.0.0.1", guest: 8000, host: 8000

    # Syncronize current folder with vangrant folder
    config.vm.synced_folder ".", "/home/vagrant"

    # Provision to install the enviroment dependency
    config.vm.provision "shell", inline: <<-SHELL
      # Update and upgrade the server packages
      sudo apt-get update
      sudo apt-get -y upgrade

      # Set Ubuntu Language
      sudo locale-gen en_GB.UTF-8
      sudo locale-gen pt_BR.UTF-8

      # Install Dependecies
      sudo apt-get install -y python3-dev sqlite python3-pip libpq-dev
      sudo apt-get install -y gettext

      # Upgrade pip to the lastest version
      sudo pip3 install --upgrade pip

      # Install and configure python virtualenvwrapper.
      sudo pip3 install virtualenvwrapper
      if ! grep -q VIRTUALENV_ALREADY_ADDED /home/ubuntu/.bashrc; then
        echo "# VIRTUALENV_ALREADY_ADDED" >> /home/ubuntu/.bashrc
        echo "WORKON_HOME=~/.virtualenvs" >> /home/ubuntu/.bashrc
        echo "PROJECT_HOME=/vagrant" >> /home/ubuntu/.bashrc
        echo "VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> /home/ubuntu/.bashrc
        echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/ubuntu/.bashrc
      fi
    SHELL
  end
end
