```mermaid
flowchart LR
  U[Client] -->|HTTP Host: api.localtest.me| LB[Cloud LoadBalancer - AKS / EKS / GKE]
  LB --> NGINX[ingress-nginx Controller Service]
  NGINX -->|Ingress rule| SVCAPI[Service: api]
  SVCAPI --> API[Deployment: api (FastAPI x2)]

  W[Deployment: worker] -->|background jobs| API

  API -->|reads/writes| SVCDB[Service: postgres]
  SVCDB --> PG[StatefulSet: postgres-0]
  PG --> PVC[PVC: data-postgres-0]
  PVC --> PV[(Cloud Disk Volume)]

  subgraph Kubernetes Cluster
    NGINX
    SVCAPI
    API
    W
    SVCDB
    PG
    PVC
  end
...
```

  subgraph Cloud Provider Storage
    PV
  end
