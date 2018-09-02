# Docker Swarm & Kubernetes commands

This is a cheatsheet for comparing Docker with Swarm and Kubernetes.

Docker Swarm is nice in it's simplicity, but lacking in it's breadth, which is where Docker with Kubernetes (Kubes) comes to play.

## Concepts and Differences

* **Nodes** - The host computers which run Docker, to run containers.  These are split as Master/Manager or Worker.
* **Groups of Services** - Swarm and Kubes both are about orchestrating services when run in a cluster of nodes working together.  In Swarm a group of services is a *Stack*, and uses the *Docker Compose* file syntax, which comes with some assumptions; where Kubes gives additional control/power, it comes with added complexity because you have to be more explicit in your definitions.  Instead of a single Docker Compose file,  you have a file with different concepts, including:
    * *Pod* - a set of resources which should be scheduled on the same node together, such as a container and a volume, or two containers.
    * *Deployment* - groups of Pods
    * *Services* - network endpoints that can be connected to pods, to publish the pod to the outside world.
* **Single Master** - Docker Swarm can be run from a single host master, where Kubes requires a more complex control plane that involves a controller, api server, scheduler and etcd.
* **Solution** vs **Toolbox** - Docker Swarm is a complete solution, where it works mostly in a single but opinionated way.  Kubes is a Toolbox, which can be configured to work in many different ways.  Because of this, you'll find Swarm works well for very specific things, and is easy to turn up.  Kubes, on the other hand, is more of a Toolbox.  It is available for others to create Solutions, but on its own it is not a solution.  This is why so many different ways are available to package and configure Kubes.  Kubes also has a package manager `helm`, which makes managing the variety of add-ons easier.
* **Command Availability** - Docker Swarm commands must be run from the docker Master nodes.  Kubectl commands can be run from either master or worker nodes.

Sometimes you want the basic features, sometimes you want the 747 cockpit.

## Tools

Docker includes all of the tools for Swarm, as part of the stock Installation.  Kubes requires additional tools, depending on the project you wish to use.

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
| Start cluster | `docker swarm init` | `kubeadm init {..}`<br>OR: `minikube start {..}`|
| Run Services (raw) | `docker service create {..}` | `kubectl run {name} {..}`<br>`kubectl expose deployment` |
| Deploy a service group | `docker stack deploy -c {cfg} {name}` | `kubectl apply -f {cfg}`|
| Console in a Container | (local to node only)<br>`docker exec -it {container} /bin/sh` | `kubectl exec -it {pod} /bin/sh` |
| Node resource usage | ? | `kubectl top node`|
| List all containers | (local to node only)<br>`docker ps {name}` | `kubectl get pods {name}`|
| List services | `docker service ls` | `kubectl get services`|
| List all containers within a service | `docker service ps {name}` | `kubectl get -n {name} pods -a`|
| Scale out | `docker service update --replicas=3 {name}`|`kubectl scale --replicas=3 deployment/{name}`|
| Update w/new Image | `docker service update --image={img} {name}`| ? |
| Pull Logs for a service | `docker service logs {name}` | `kubectl logs {name}` |
| Port Forward to remote container | n/a | `kubectl port-forward` |

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

Equivalent in Kubes as a Deployment with file `node-hello-kubes.yml`:

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
