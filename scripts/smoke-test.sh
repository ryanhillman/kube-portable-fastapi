#!/usr/bin/env bash
set -euo pipefail

# local test assumes kind + ingress installed and host api.localtest.me
curl -sS http://api.localtest.me/healthz
curl -sS -X POST http://api.localtest.me/jobs -H 'Content-Type: application/json' -d '{"hello":"world"}'
curl -sS http://api.localtest.me/jobs/next
echo
echo "OK"