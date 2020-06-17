# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  ENV["LC_ALL"] = "en_US.UTF-8"

  # Define base box
  config.vm.box = "ubuntu/bionic64"
  config.vm.define 'dhcpspoof'
  config.vm.hostname = 'dhcpspoof'
  config.vm.box_check_update = false

  # VB Guest Additions configuration:
  if Vagrant.has_plugin?('vagrant-vbguest')
    config.vbguest.auto_reboot = true
  else
    puts '.'
    puts 'WARN: Could not find vagrant-vbguest plugin.'
    puts 'INFO: This plugin is highly recommended as it ensures that your VB guest additions are up-to-date.'
    puts 'INFO: $ vagrant plugin install vagrant-vbguest'
    puts '.'
  end

  # Virtualbox specific configuration
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "2"
  end

  # Enable X forwarding
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true

  config.vm.provision "shell", path: "vagrantsh/installcore.sh"

  config.trigger.after :up, :reload do |trigger|
    trigger.info = "More information"
    trigger.run_remote = {
      path: './vagrantsh/bootstrap.sh'
    }
  end

end
