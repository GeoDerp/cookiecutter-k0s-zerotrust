#!/bin/bash
set -e

if ! command -v kubectl &> /dev/null; then
    echo "kubectl could not be found. Please use 'k0s kubectl' or install kubectl."
    exit 1
fi

echo ">>> Bootstrapping ArgoCD..."

# 3.2 Installing ArgoCD
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/{{ cookiecutter.argocd_version }}/manifests/install.yaml

echo ">>> Waiting for ArgoCD components..."
kubectl wait --for=condition=Available deployment/argocd-server -n argocd --timeout=300s

# Apply the Root App (App of Apps)
echo ">>> Applying Root Application..."
kubectl apply -f gitops/bootstrap/root-app.yaml

echo ">>> ArgoCD Bootstrap complete."
echo "Get the admin password:"
echo "kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d"
