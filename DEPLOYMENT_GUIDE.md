# 🚀 Cyber Defense Application Deployment Guide

This guide covers deploying your application using Docker Compose and Kubernetes orchestration.

## 📋 Prerequisites

- **Docker Desktop** installed and running
- **kubectl** installed (for Kubernetes)
- **Kubernetes cluster** (Docker Desktop includes one)

## 🐳 Docker Deployment

### Development Environment

```bash
# Run the development stack
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop the stack
docker-compose -f docker-compose.dev.yml down
```

### Production Environment

```bash
# Run the production stack
docker-compose -f backend/deployment/docker-compose.prod.yml up -d

# View logs
docker-compose -f backend/deployment/docker-compose.prod.yml logs -f

# Stop the stack
docker-compose -f backend/deployment/docker-compose.prod.yml down
```

## ☸️ Kubernetes Orchestration

### Step 1: Enable Kubernetes in Docker Desktop
1. Open Docker Desktop
2. Go to Settings > Kubernetes
3. Check "Enable Kubernetes" 
4. Click "Apply & Restart"

### Step 2: Deploy to Kubernetes

```bash
# Make the deployment script executable
chmod +x deploy-k8s.sh

# Run the deployment
./deploy-k8s.sh
```

### Step 3: Manual Deployment (Alternative)

```bash
# Create namespace
kubectl apply -f backend/deployment/k8s/namespace.yaml

# Deploy database and services
kubectl apply -f backend/deployment/k8s/database.yaml
kubectl apply -f backend/deployment/k8s/services.yaml

# Deploy main application
kubectl apply -f backend/deployment/k8s/deployment.yaml
```

## 📊 Viewing Docker Logs

### Docker Compose Logs
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis

# View logs with timestamps
docker-compose logs -f -t

# View last 100 lines
docker-compose logs --tail=100 -f
```

### Individual Container Logs
```bash
# List running containers
docker ps

# View logs for specific container
docker logs -f <container_name_or_id>

# Example:
docker logs -f luckniteshoots_backend_1
```

### Docker Desktop GUI Logs
1. Open Docker Desktop
2. Go to "Containers" tab
3. Click on your container
4. View logs in the "Logs" tab
5. Logs update in real-time

## 📊 Viewing Kubernetes Logs

### Pod Logs
```bash
# List pods
kubectl get pods -n cyber-defense

# View logs for specific pod
kubectl logs -f <pod-name> -n cyber-defense

# View logs for deployment
kubectl logs -f deployment/cyber-defense-backend -n cyber-defense

# View logs for all containers in a pod
kubectl logs -f <pod-name> --all-containers -n cyber-defense
```

### Service Status
```bash
# View all resources
kubectl get all -n cyber-defense

# View pod status
kubectl get pods -n cyber-defense

# View service status
kubectl get services -n cyber-defense

# Describe pod for detailed info
kubectl describe pod <pod-name> -n cyber-defense
```

## 🔗 Accessing Services

### Docker Compose
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Database**: localhost:5432
- **Redis**: localhost:6379
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001

### Kubernetes
```bash
# Port forward to access services locally
kubectl port-forward service/backend-service 8000:8000 -n cyber-defense
kubectl port-forward service/frontend-service 3000:3000 -n cyber-defense

# Then access:
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## 🛠️ Troubleshooting

### Docker Issues
```bash
# Check Docker status
docker info

# Restart Docker Compose
docker-compose down && docker-compose up -d

# View container resource usage
docker stats

# Clean up unused resources
docker system prune -a
```

### Kubernetes Issues
```bash
# Check cluster info
kubectl cluster-info

# Check node status
kubectl get nodes

# View events
kubectl get events -n cyber-defense --sort-by='.lastTimestamp'

# Delete and redeploy
kubectl delete namespace cyber-defense
./deploy-k8s.sh
```

## 📈 Monitoring

### Prometheus Metrics
- Access: http://localhost:9090 (Docker) or port-forward for K8s
- Query examples:
  - `up` - Service availability
  - `http_requests_total` - Request metrics
  - `container_memory_usage_bytes` - Memory usage

### Grafana Dashboards
- Access: http://localhost:3001 (Docker) or port-forward for K8s
- Default credentials: admin/admin (set in environment)
- Pre-configured dashboards for application metrics

## 🔄 Scaling

### Docker Compose
```bash
# Scale backend service
docker-compose up -d --scale backend=3
```

### Kubernetes
```bash
# Scale deployment
kubectl scale deployment cyber-defense-backend --replicas=5 -n cyber-defense

# Auto-scaling (HPA)
kubectl autoscale deployment cyber-defense-backend --cpu-percent=50 --min=1 --max=10 -n cyber-defense
```

## 🧹 Cleanup

### Docker
```bash
# Stop and remove containers
docker-compose down -v

# Remove images
docker rmi $(docker images -q)
```

### Kubernetes
```bash
# Delete namespace (removes all resources)
kubectl delete namespace cyber-defense

# Or delete specific resources
kubectl delete -f backend/deployment/k8s/
```