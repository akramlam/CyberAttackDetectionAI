#!/bin/bash

echo "🚀 Deploying Cyber Defense Application to Kubernetes"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Build Docker images
echo "📦 Building Docker images..."
docker build -t cyber-defense-backend:latest ./backend
# docker build -t cyber-defense-frontend:latest ./frontend
# docker build -t cyber-defense-ml:latest ./ml_engine

# Apply Kubernetes manifests
echo "☸️  Applying Kubernetes manifests..."

# Create namespace first
kubectl apply -f backend/deployment/k8s/namespace.yaml

# Apply database and services
kubectl apply -f backend/deployment/k8s/database.yaml
kubectl apply -f backend/deployment/k8s/services.yaml

# Apply main deployment
kubectl apply -f backend/deployment/k8s/deployment.yaml

echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n cyber-defense --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n cyber-defense --timeout=300s
kubectl wait --for=condition=ready pod -l app=cyber-defense-backend -n cyber-defense --timeout=300s

echo "✅ Deployment complete!"

# Show status
echo "📊 Current status:"
kubectl get pods -n cyber-defense
kubectl get services -n cyber-defense

echo ""
echo "🔍 To view logs:"
echo "kubectl logs -f deployment/cyber-defense-backend -n cyber-defense"
echo ""
echo "🌐 To access the application:"
echo "kubectl port-forward service/backend-service 8000:8000 -n cyber-defense"