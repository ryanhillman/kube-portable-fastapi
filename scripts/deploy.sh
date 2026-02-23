#!/usr/bin/env bash
set -euo pipefail
OVERLAY="${1:-local}"

kubectl apply -k "k8s/overlays/${OVERLAY}"

kubectl -n portable rollout status statefulset/postgres --timeout=180s
kubectl -n portable rollout status deploy/api --timeout=180s
kubectl -n portable rollout status deploy/worker --timeout=180s