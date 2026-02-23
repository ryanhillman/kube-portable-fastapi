#!/usr/bin/env bash
set -euo pipefail

kind create cluster --name portable || true

# Install ingress-nginx for kind (uses NodePort; no cloud LB)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s