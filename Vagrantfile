NODES = [
	["manager1", "192.168.189.100", "manager"],
	["manager2", "192.168.189.101", "manager"],
	["manager3", "192.168.189.102", "manager"],
]

Vagrant.configure("2") do |config|
	manager_ip = ""
	manager_token = ""
	worker_token = ""
	NODES.each do |(node_name, ip_address, role)|
		config.vm.define node_name do |node|
			node.vm.box = "bento/ubuntu-20.04"
			node.vm.hostname = node_name
			node.vm.network "private_network", ip: ip_address

			node.vm.provider "vmware_desktop" do |v|
				v.vmx["displayname"] = node_name
				v.vmx["memsize"] = "1024"
				v.vmx["numvcpus"] = "1"
			end
			
			if defined? ENV["VAGRANT_SSH_PUB_KEY"] == nil
				ENV["VAGRANT_SSH_PUB_KEY"] = "#{Dir.home}/.ssh/id_ed25519.pub"
			end

			ssh_pub_key = File.readlines(ENV["VAGRANT_SSH_PUB_KEY"]).first.strip
			node.vm.provision "SSH_KEY", type: "shell",
				inline: <<-SHELL
					echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
				SHELL

			node.vm.provision "Docker Daemon Install", type: "shell",
				inline: <<-SHELL
					# Faire en sorte que les machines puissent communiquer entre elles via leur hostnames (exemple: ping worker1 depuis manager1)
					#{NODES.map{ |n_name, ip| "echo '#{ip} #{n_name}' | sudo tee -a /etc/hosts\n"}.join}

					# Installer Docker
					curl -fsSL get.docker.com -o get-docker.sh
					CHANNEL=stable sh get-docker.sh
					rm get-docker.sh
				SHELL
			
			vagrant_docker_unsafe = ENV["VAGRANT_DOCKER_UNSAGE"] || "false"
			if vagrant_docker_unsafe != "false" 
				node.vm.provision "Docker Daemon API", type: "shell", after: "Docker Daemon Install",
				inline: <<-SHELL
					# Faire en sorte que le daemon Docker soit accessible depuis l'hôte
					sudo mkdir -p /etc/systemd/system/docker.service.d
					sudo bash -c 'echo -e "[Service]\nExecStart=\nExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375" > /etc/systemd/system/docker.service.d/options.conf'
					sudo systemctl daemon-reload
					sudo systemctl restart docker.service
				SHELL
			end

			# Don't Work
			docker_registry_url = ENV["DOCKER_REGISTRY_URL"] || "false"
			if docker_registry_url != "false"
				docker_registry_username = ENV["DOCKER_REGISTRY_USERNAME"]
				docker_registry_password = ENV["DOCKER_REGISTRY_PASSWORD"]  
				node.vm.provision "Docker Regsitry", type: "shell", after: "Docker Daemon Install",
					inline: <<-SHELL
						echo #{docker_registry_password} | docker login \
							--username=#{docker_registry_username}
							--password-stdin
							#{docker_registry_url}
					SHELL
			end

			node.vm.provision "docker" do |d|
				d.pull_images "alpine:latest"
			end
		end
	end
end