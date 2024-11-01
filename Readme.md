
# Projet API Flask avec Kubernetes

## Prérequis

- Minikube : pour créer un cluster Kubernetes local.
- kubectl : l'outil en ligne de commande pour interagir avec Kubernetes.
- Docker : pour construire les images Docker.

## Étapes de déploiement

### 1. Construire l'image Docker

Naviguer dans le dossier contenant le `Dockerfile`, puis exécutez la commande suivante pour construire l'image Docker :

```bash
docker build -t weleassane/car-api-image:v1.0.0 .
```
#### Remarque:
J'ai gardé Python:3.9 au lieu d'utiliser Python:3.9-alpine car si je l'utilise, l'image ne build pas et renvoie des erreurs. A ce qu'il parait, ceci est causé par les requirements du flask.
### 2. Lancer Minikube

Démarrez Minikube avec 3 nœuds :

```bash
minikube start --nodes 3 --driver=docker
```

### 3. Appliquer les manifestes Kubernetes

Naviguez jusqu'au dossier contenant les fichiers manifestes Kubernetes (`k8s`) et appliquez-les avec les commandes suivantes :

```bash
kubectl apply -f k8s/database-deployment.yaml
kubectl apply -f k8s/database-service.yaml
kubectl apply -f k8s/database-secret.yaml
kubectl apply -f k8s/database-configmap.yaml
kubectl apply -f k8s/backend-configmap.yaml
kubectl apply -f k8s/backend-secret.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
```

### 4. Vérifier le déploiement

Pour vérifier que les pods sont en cours d'exécution, utilisez la commande :

```bash
kubectl get pods
```

### 5. Accéder à l'API

Exposez le service backend via un NodePort pour accéder à l'API :

```bash
minikube service backend-service --url
```

Cela vous donnera l'URL que vous pouvez utiliser pour interagir avec l'API.

### 6. Points de terminaison

- **Ajouter une voiture :**

```bash
curl -X POST http://<adresse_node>:<port>/car-api/post-car -H "Content-Type: application/json" -d '{"brand": "Toyota", "colour": "Red"}'
```

- **Lister toutes les voitures :**

```bash
curl http://<adresse_node>:<port>/car-api/get-cars
```

- **Vérifier la santé de l'application :**

  - **Liveness probe :** `/health/live`
  - **Readiness probe :** `/health/ready`
