# Docker Swarm & Kubernetes commands

This is a cheatsheet for comparing Docker with Swarm and Kubernetes.

Docker Swarm is nice in it's simplicity, but lacking in it's breadth, which is where Docker with Kubernetes comes to play.

## Concepts

* **Nodes** - The host computers which run Docker, to run containers.
* **Groups of Services** - Swarm and Kubernetes both are about orchestrating services when run in a cluster of nodes working together.  In Swarm a group of services is a *Stack*, and uses the *Docker Compose* file syntax, which comes with some assumptions; where Kubernetes gives additional control/power, it comes with added complexity because you have to be more explicit in your definitions.  Instead of a single Docker Compose file,  you have a file with different concepts, including:
    * *Pod* - a set of resources which should be scheduled on the same node together, such as a container and a volume, or two containers.
    * *Deployment* - groups of Pods
    * *Services* - network endpoints that can be connected to pods, to publish the pod to the outside world.

Sometimes you want the basic features, sometimes you want the 747 cockpit.

## Tools

Docker includes all of the tools for Swarm, as part of the stock Installation.  Kubernetes requires additional tools, depending on the project you wish to use.

* [kubeadm](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/#24-initializing-your-master)
* [minikube](https://kubernetes.io/docs/getting-started-guides/minikube/)


## Comparisons

This is a WIP, please contact me with any corrections/updates you may feel are appropriate.  Thanks!

| Concept| Swarm | Kubes|
| ----- |----|-----|
| Management Nodes | Manager | Master |
| Container+Volume | Docker Compose File | Pod |
| Group of services | Docker Compose File | Deployment |
| Config File | see below| see below|
| Start cluster | docker swarm init | kubeadm init<br> minikube start|
| Run Services (raw) | docker service create {..} | kubectl run {name} {..}<br>kubectl expose deployment|
| Deploy a service group | docker stack deploy -c {cfg} {name} | kubectl apply -f {cfg}|
| Console in a Container | (limit: to node)<br>docker exec -it {container} /bin/bash| kubectl exec -it {pod} /bin/bash|
| Node resource usage | | kubectl top node|
| List all containers | (per node)<br>docker ps| kubectl get pods|
| List services | docker service ls | kubectl get services|
| List all containers within a service | docker service ps {name} | kubectl get -n {name} pods -a|
| Scale out | docker service update --replicas=3 {name}|kubectl scale --replicas=3 deployment/{name}|
| Pull Logs for a service | docker service logs {name} | |

Docker Swarm Stack file `node-hello-swarm.yml`:

<pre>
version: "3.3"
services:
  hello:
    image: node-hello:tst
    ports:
      - "8080"
    environment:
      - PORT=8080
    deploy:
      replicas: 2
</pre>

Deployed with:
```bash
docker stack deploy -c node-hello-swarm.yml node-hello
docker service ps node-hello
```

Equivalent in Kubernetes as a Deployment with file `node-hello-kubes.yml`:

<pre>
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-hello-deployment
  labels:
    app: node-hello
spec:
  replicas: 2
  selector:
    matchLabels:
      app: node-hello
  template:
    metadata:
      labels:
        app: node-hello
    spec:
      containers:
      - name: node-hello
        image: node-hello:tst
        ports:
        - containerPort: 8080
</pre>

Deployed with:

```bash
kubectl create -f node-hello-kubes.yml
kubectl get deployments
kubectl rollout status deployment/node-hello-deployment
kubectl get pods --show-labels {...}
```
