#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting deployment of Stock Analysis System...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p services/monitoring/grafana/dashboards

# Build and deploy using Docker Compose
echo "Building and deploying services..."
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "Checking service status..."
services=("frontend" "api" "scheduler" "mongodb" "redis" "prometheus" "grafana")
for service in "${services[@]}"; do
    if docker-compose ps | grep -q "$service.*Up"; then
        echo -e "${GREEN}✓ $service is running${NC}"
    else
        echo -e "${RED}✗ $service failed to start${NC}"
    fi
done

# Initialize MongoDB indexes
echo "Initializing MongoDB indexes..."
docker-compose exec mongodb mongo stock_analysis --eval '
    db.stocks.createIndex({ symbol: 1 }, { unique: true });
    db.stocks.createIndex({ recommendation: 1 });
    db.stocks.createIndex({ risk: 1 });
    db.sentiment.createIndex({ symbol: 1, timestamp: -1 });
'

# Set up Grafana dashboards
echo "Setting up Grafana dashboards..."
curl -X POST \
    -H "Content-Type: application/json" \
    -d @services/monitoring/grafana/dashboards/stock-metrics.json \
    http://admin:admin@localhost:3001/api/dashboards/db

echo -e "\n${GREEN}Deployment completed!${NC}"
echo "Access the services at:"
echo "- Frontend: http://localhost:3000"
echo "- API Docs: http://localhost:8000/docs"
echo "- Grafana: http://localhost:3001 (admin/admin)"
echo "- Prometheus: http://localhost:9090"

# Monitor logs
echo -e "\n${GREEN}Monitoring logs...${NC}"
docker-compose logs -f
