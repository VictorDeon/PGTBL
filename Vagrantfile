Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.define :tbl do |web_config|
    config.vm.network "private_network", ip: "192.168.50.4"
    config.vm.network "forwarded_port", guest: 8000, host: 8000
    config.vm.provision "shell", path: "scripts/bootstrap.sh"
  end
end
