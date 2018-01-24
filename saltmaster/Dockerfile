FROM centos:7

RUN yum -y install https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm && \
    yum -y install salt-master  iproute

WORKDIR /srv

COPY pillar /srv/pillar
COPY salt /srv/salt

#RUN echo 192.168.63.128 tombstone >> /etc/hosts
RUN echo 172.18.0.3 tombstone >> /etc/hosts

ENTRYPOINT [ "/usr/bin/salt-master" ]
