# Deployment Guide 🚀

## Overview 🌐

This guide covers deployment strategies and configurations for the AWS Orchestrator platform.

## Deployment Architecture 🏗️

```mermaid
graph TB
    subgraph Production
        LB[Load Balancer]
        API1[API Server 1]
        API2[API Server 2]
        Cache[(Redis Cache)]
        DB[(Database)]
        Queue[(Message Queue)]
    end
    
    subgraph AWS
        S3[S3 Storage]
        Lambda[Lambda Functions]
        SQS[SQS Queue]
    end
    
    LB --> API1
    LB --> API2
    API1 --> Cache
    API2 --> Cache
    API1 --> DB
    API2 --> DB
    API1 --> Queue
    API2 --> Queue
    Queue --> Lambda
    Lambda --> S3
    Lambda --> SQS
    
    style Production fill:#f9f,stroke:#333
    style AWS fill:#9cf,stroke:#333
```

## Environment Setup ⚙️

### 1. Environment Variables
```bash
# .env.production
NODE_ENV=production
API_PORT=8000
DB_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
AWS_REGION=us-east-1
LOG_LEVEL=info
```

### 2. Configuration Management
```python
# config/production.py
class ProductionConfig:
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv('DB_URL')
    REDIS_URI = os.getenv('REDIS_URL')
    AWS_CONFIG = {
        'region': os.getenv('AWS_REGION'),
        'api_version': '2023-01-01'
    }
```

## Container Configuration 🐳

### 1. Dockerfile
```dockerfile
# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "app:app", "--workers", "4", "--bind", "0.0.0.0:8000"]
```

### 2. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_URL=${DB_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
  
  redis:
    image: redis:6
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Kubernetes Deployment 🎮

### 1. API Deployment
```yaml
# k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aws-orchestrator-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aws-orchestrator-api
  template:
    metadata:
      labels:
        app: aws-orchestrator-api
    spec:
      containers:
      - name: api
        image: aws-orchestrator:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_URL
          valueFrom:
            secretKeyRef:
              name: aws-orchestrator-secrets
              key: db-url
```

### 2. Service Configuration
```yaml
# k8s/api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: aws-orchestrator-api
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: aws-orchestrator-api
```

## CI/CD Pipeline 🔄

### 1. GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy AWS Orchestrator

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Build and push Docker image
      run: |
        docker build -t aws-orchestrator .
        docker tag aws-orchestrator:latest ${{ secrets.ECR_REGISTRY }}/aws-orchestrator:latest
        docker push ${{ secrets.ECR_REGISTRY }}/aws-orchestrator:latest
    
    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --name aws-orchestrator-cluster
        kubectl apply -f k8s/
```

## Monitoring Setup 📊

### 1. Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'aws-orchestrator'
    static_configs:
      - targets: ['localhost:8000']
```

### 2. Grafana Dashboard
```json
{
  "dashboard": {
    "title": "AWS Orchestrator Production",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "http_request_duration_seconds"
          }
        ]
      }
    ]
  }
}
```

## Backup Strategy 💾

### 1. Database Backup
```bash
#!/bin/bash
# backup.sh

# Set variables
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump $DB_URL > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

# Upload to S3
aws s3 cp $BACKUP_DIR/db_backup_$TIMESTAMP.sql s3://backups/
```

### 2. Backup Schedule
```yaml
# k8s/backup-cronjob.yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: db-backup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-tool:latest
            command: ["/scripts/backup.sh"]
```

## Scaling Strategy 📈

### 1. Horizontal Pod Autoscaling
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: aws-orchestrator-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: aws-orchestrator-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      targetAverageUtilization: 70
```

### 2. Vertical Pod Autoscaling
```yaml
# k8s/vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: aws-orchestrator-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: aws-orchestrator-api
  updatePolicy:
    updateMode: Auto
```

## Best Practices 📚

1. **Deployment**
   - Blue-green deployment
   - Canary releases
   - Rolling updates
   - Automated rollbacks

2. **Security**
   - Secret management
   - Network policies
   - Security groups
   - SSL/TLS configuration

3. **Monitoring**
   - Health checks
   - Resource monitoring
   - Alert configuration
   - Log aggregation

4. **Maintenance**
   - Regular backups
   - Update strategy
   - Disaster recovery
   - Performance optimization
