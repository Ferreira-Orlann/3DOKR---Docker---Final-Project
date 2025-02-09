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

			node.vm.provision "Docker Install and /etc/hosts", type: "shell",
				inline: <<-SHELL
					# Faire en sorte que les machines puissent communiquer entre elles via leur hostnames (exemple: ping worker1 depuis manager1)
					#{NODES.map{ |n_name, ip| "echo '#{ip} #{n_name}' | sudo tee -a /etc/hosts\n"}.join}

					# Installer Docker
					curl -fsSL get.docker.com -o get-docker.sh
					CHANNEL=stable sh get-docker.sh
					rm get-docker.sh

					sudo docker plugin install --grant-all-permissions --alias gluster-stack-data chrisbecke/glusterfs-volume GFS_VOLUME=stack-data GFS_SERVERS=manager1,manager2,manager3 || exit 0 && sudo docker plugin enable gluster-stack-data
				SHELL
			
			node.vm.provision "Gluster FS Init & Enable Plugin", type: "shell",
				inline: <<-SHELL
					sudo apt install -y glusterfs-server
					sudo systemctl enable --now glusterd
					sudo mkdir -p /var/local/stack-data

					# sudo docker plugin enable gluster-stack-data
				SHELL
		end
	end

	config.vm.define "manager1" do |vm| 
		vm.vm.provision "Docker Swarm Init and ", type: "shell",
				inline: <<-SHELL
					docker swarm init --advertise-addr #{NODES[0][1]}
					sudo docker swarm join-token -q manager > /vagrant/docker-token.txt
				SHELL
	end
	
	config.vm.define "manager2" do |vm|
		vm.vm.provision "Swarm Join", type: "shell",
				inline: <<-SHELL
					docker swarm join --token $(cat /vagrant/docker-token.txt) #{NODES[0][1]}:2377
				SHELL
	end

	config.vm.define "manager3" do |vm| 
		vm.vm.provision "Swarm Join", type: "shell",
				inline: <<-SHELL
					docker swarm join --token $(cat /vagrant/docker-token.txt) #{NODES[0][1]}:2377
				SHELL
	end

	config.vm.define "manager3" do |vm| 
		vm.vm.provision "GlusterFS Volume Create and Docker Stack Stack", type: "shell",
				inline: <<-SHELL
					cd /vagrant

					sudo gluster peer probe manager1
					sudo gluster peer probe manager2
					sudo gluster peer probe manager3
					sudo gluster volume create stack-data replica 3 manager1:/var/local/stack-data manager2:/var/local/stack-data manager3:/var/local/stack-data force

					sudo gluster volume set stack-data performance.stat-prefetch off
					sudo gluster volume set stack-data performance.read-ahead off
					sudo gluster volume set stack-data performance.write-behind off
					sudo gluster volume set stack-data performance.readdir-ahead off
					sudo gluster volume set stack-data performance.io-cache off
					sudo gluster volume set stack-data performance.quick-read off
					sudo gluster volume set stack-data performance.open-behind off
					sudo gluster volume set stack-data performance.strict-o-direct on

					sudo gluster volume start stack-data

					# sudo docker stack deploy -c docker-compose.yml appstack
				SHELL
	end
end