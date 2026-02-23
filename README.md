## Architecture

```mermaid
flowchart LR
  U[Client] -->|HTTP Host: api.localtest.me| LB[Cloud LoadBalancer<br/>AKS / EKS / GKE]
  LB --> NGINX[ingress-nginx Controller<br/>(Service: LoadBalancer)]
  NGINX -->|Ingress rule: api.localtest.me| SVCAPI[Service: api]
  SVCAPI --> API[Deployment: api<br/>FastAPI pods x2]

  W[Deployment: worker] -->|background jobs| API

  API -->|reads/writes| SVCDB[Service: postgres]
  SVCDB --> PG[StatefulSet: postgres-0]
  PG --> PVC[PVC: data-postgres-0]
  PVC --> PV[(Cloud Disk)]

  subgraph K8s[Kubernetes Cluster]
    NGINX
    SVCAPI
    API
    W
    SVCDB
    PG
    PVC
  end

  subgraph Cloud[Cloud Provider Storage]
    PV
  end
