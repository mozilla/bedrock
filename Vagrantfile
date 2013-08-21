# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "precise32"
  config.vm.box_url = "http://people.mozilla.com/~bsternthal/vagrant/precise32.box" 

  # Add to /etc/hosts: 192.168.10.55 local.mozilla.org
  config.vm.network :private_network, ip: "192.168.10.55"

  config.ssh.max_tries = 3
  config.ssh.timeout = 1000

  # Not sure if really needed but leaving in
  config.vm.network :forwarded_port, guest: 8000, host: 8000

  #manually set this due to permissions and lessc
  config.vm.synced_folder ".", "/vagrant", :owner => "www-data", :extra => 'dmode=775,fmode=664'
  config.vm.synced_folder "../mozilla.com", "/srv/legacy", :owner => "www-data", :extra => 'dmode=775,fmode=664'

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.manifest_file = "vagrant.pp"
  end  

end
