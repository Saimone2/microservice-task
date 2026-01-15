# FastAPI Microservice with MinIO & MikroK8s

## Overview
This project demonstrates deploying a Python FastAPI microservice in a **MikroK8s** cluster with **MinIO** as an S3‑compatible storage backend.  
The microservice provides API endpoints to manage buckets: create, retrieve information, and delete.

## API Endpoints
- **GET /api/bucket/{uuid}**  
  Returns a JSON object with the total number of objects and their combined size in the bucket.

- **POST /api/bucket/{uuid}**  
  Creates a new bucket in MinIO and returns a status response.

- **DELETE /api/bucket/{uuid}**  
  Deletes the specified bucket and returns a status response.

## Tech Stack
- Python 3.13.5 / FastAPI
- Boto3 (S3 client for MinIO)
- Pytest (unit testing)
- Docker
- MikroK8s (Kubernetes)
- GitHub Actions (CI)

## Prerequisites & Configuration
1. **Environment Requirements**
- VM or server with MikroK8s installed and running.
- Docker installed and configured to push images to the local registry (localhost:32000).
- MinIO deployed in the cluster as an S3‑compatible storage backend.

2. **MinIO Setup**
- Deploy MinIO in MikroK8s.
- Create an access key and secret key for the S3 client.
- Expose MinIO service internally.

3. **Kubernetes Manifests**
- ```microservice-deployment.yaml``` → defines the FastAPI pod and environment variables.
- ```microservice-service.yaml``` → exposes the microservice inside the cluster.
- ```ingress.yaml``` → provides external access via HTTP.

5. **Deployment Steps**
- Build and push Docker image

  ```docker build -t localhost:32000/microservice-task:latest . ```

  ```docker push localhost:32000/microservice-task:latest``` 

- Apply manifests

  ```microk8s kubectl apply -f k8s/microservice-deployment.yaml```

  ```microk8s kubectl apply -f k8s/microservice-service.yaml```

  ```microk8s kubectl apply -f k8s/ingress.yaml```
