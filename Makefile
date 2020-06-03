# commands for DevOps

#### commands for docker

# get latest script to install docker
install-get-docker-script:
	curl -fsSL get.docker.com -o ./scripts/get-docker.sh
	chmod +x ./scripts/get-docker.sh

# use ./scripts/get-docker.sh to install docker
install-docker:
	sudo sh ./scripts/get-docker.sh --mirror Aliyun

# enable docker service
enable-docker:
	sudo systemctl enable docker

# disable docker service
disable-docker:
	sudo systemctl disable docker

# start docker service
start-docker: enable-docker
	sudo systemctl start docker

# stop docker service
stop-docker: enable-docker
	sudo systemctl stop docker

#### end of commands for docker

#### commands for management scripts

install-gov-shell:
	sudo -H pip3 install fire

gov-shell:
	./bin/minimum

help-gov-shell:
	./bin/minimum help

get-config:
	./bin/minimum make context
#### end of commands for management scripts


.PHONY: \
	install-docker install-get-docker-script\
	enable-docker disable-docker start-docker stop-docker\
	gov-shell help-gov-shell install-gov-shell get-config