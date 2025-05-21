# FastAPI Vue Helm Chart

This Helm chart deploys a FastAPI backend with a Vue.js frontend, using Caddy as a reverse proxy.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
helm install my-release ./helm/fastapivue
```

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
helm delete my-release
```

## Configuration

The following table lists the configurable parameters of the FastAPI Vue chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount.backend` | Number of backend replicas | `1` |
| `replicaCount.frontend` | Number of frontend replicas | `1` |
| `replicaCount.caddy` | Number of caddy replicas | `1` |
| `image.backend.repository` | Backend image repository | `myorg/backend` |
| `image.backend.tag` | Backend image tag | `latest` |
| `image.backend.pullPolicy` | Backend image pull policy | `IfNotPresent` |
| `image.frontend.repository` | Frontend image repository | `myorg/frontend` |
| `image.frontend.tag` | Frontend image tag | `latest` |
| `image.frontend.pullPolicy` | Frontend image pull policy | `IfNotPresent` |
| `image.caddy.repository` | Caddy image repository | `caddy` |
| `image.caddy.tag` | Caddy image tag | `latest` |
| `image.caddy.pullPolicy` | Caddy image pull policy | `IfNotPresent` |
| `service.backend.type` | Backend service type | `ClusterIP` |
| `service.backend.port` | Backend service port | `8010` |
| `service.frontend.type` | Frontend service type | `ClusterIP` |
| `service.frontend.port` | Frontend service port | `5000` |
| `service.caddy.type` | Caddy service type | `ClusterIP` |
| `service.caddy.port` | Caddy service port | `80` |
| `service.caddy.nodePort` | Caddy service nodePort (if type is NodePort) | `30080` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.hosts` | Ingress hosts | `[{host: fastapivue.local, paths: [{path: /, pathType: Prefix}]}]` |
| `ingress.tls` | Ingress TLS configuration | `[]` |
| `resources` | CPU/Memory resource requests/limits | See `values.yaml` |
| `autoscaling.enabled` | Enable autoscaling | `false` |
| `autoscaling.minReplicas` | Minimum number of replicas | `1` |
| `autoscaling.maxReplicas` | Maximum number of replicas | `10` |
| `autoscaling.targetCPUUtilizationPercentage` | Target CPU utilization percentage | `80` |
| `nodeSelector` | Node selector | `{}` |
| `tolerations` | Tolerations | `[]` |
| `affinity` | Affinity | `{}` |
| `env.common` | Common environment variables | `{}` |
| `env.backend` | Backend-specific environment variables | `{}` |
| `env.frontend` | Frontend-specific environment variables | `{}` |

## Architecture

The chart deploys three main components:

1. **Backend**: A FastAPI service that handles API requests.
2. **Frontend**: A Vue.js application that serves the user interface.
3. **Caddy**: A reverse proxy that routes traffic between the frontend and backend.

Caddy is configured to route requests starting with `/api/*` to the backend service, and all other requests to the frontend service.

## Examples

### Custom Environment Variables

```yaml
env:
  common:
    DEBUG: "true"
  backend:
    DATABASE_URL: "postgresql://user:password@postgres:5432/db"
  frontend:
    API_URL: "/api"
```

### Custom Ingress Configuration

```yaml
ingress:
  enabled: true
  className: "nginx"
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com
```
