# Saltception

Running Salt Master inside a containe which manages the parent host outside the container.

This is an example of how to leverage containers even for things such as a salt master.

This is intended as a reference, run as a swarm service, on a single node with local storage (or shared if you want to put it into a cluster).

In this setup you have two entities:

1. outside server running Docker, and a Salt Minion (the Host)
2. inside container running Salt Master (the Container)

# Setup the Master (Container)

Assertion: Docker is already setup on the Host, and Docker Compose is available.

1. Get the container

    git clone github...link

2. Build and run the container

    cd saltmaster
    docker-compose up --build

# Setup the Host

1. Install Docker
2. Setup some persistent folders to use as volume mounts into the container:

    base=/data/saltmaster # you can specify this wherever; just update your stackfile
    sudo mkdir -p $base/{pki,cache,log}

3. Install Salt Minion

    # if centos/rhel
    yum -y install salt-minion

    # if debian/ubuntu
    apt -y install salt-minion

4. Configure minion

    echo 127.0.0.1 salt >> /etc/hosts
    echo 'publish_port: 4057' >> /etc/salt/minion.d/local-minion.conf

5. Start the minion

    systemctl start salt-minion

# updates to the service

    docker build -t salt-master . && \
        docker service update salt_master --image=salt-master --force

(one might suggest you have a CI system trigger this command on a merge to a git repo)

