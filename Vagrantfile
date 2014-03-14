# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_version ">= 1.4.0"

Vagrant.configure("2") do |config|

  config.vm.box = "precise32"
  config.vm.box_url = "http://people.mozilla.com/~bsternthal/vagrant/precise32.box"

  # Add to /etc/hosts: 192.168.10.55 mozilla.local
  config.vm.network :private_network, ip: "192.168.10.55"

  # Not sure if really needed but leaving in
  config.vm.network :forwarded_port, guest: 8000, host: 8000

  # Manually set permissions for to allow writing
  config.vm.synced_folder ".", "/vagrant", :owner => "www-data", :mount_options => ['dmode=775','fmode=664']
  config.vm.synced_folder "../mozilla.com", "/srv/legacy", :owner => "www-data", :mount_options => ['dmode=775','fmode=664']

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.manifest_file = "vagrant.pp"
  end

end
