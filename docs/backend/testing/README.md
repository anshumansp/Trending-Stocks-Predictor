# Backend Testing Guide 🧪

## Overview 🌐

This guide covers testing strategies and implementations for the AWS Orchestrator backend.

## Test Structure 📁

```
tests/
├── unit/              # Unit tests
│   ├── api/          # API tests
│   ├── services/     # Service tests
│   └── utils/        # Utility tests
├── integration/       # Integration tests
│   ├── aws/         # AWS integration
│   └── database/    # Database integration
└── e2e/              # End-to-end tests
```

## Unit Testing 🔬

### 1. API Tests
```python
# tests/unit/api/test_resource_api.py
import pytest
from app.api import resource_api

def test_create_resource():
    """Test resource creation endpoint"""
    payload = {
        "type": "ec2",
        "config": {
            "instance_type": "t2.micro",
            "region": "us-east-1"
        }
    }
    response = resource_api.create_resource(payload)
    assert response.status_code == 201
    assert "resource_id" in response.json
```

### 2. Service Tests
```python
# tests/unit/services/test_aws_service.py
from unittest.mock import Mock, patch
from app.services import aws_service

@patch('boto3.client')
def test_ec2_instance_creation(mock_boto):
    """Test EC2 instance creation"""
    mock_ec2 = Mock()
    mock_boto.return_value = mock_ec2
    
    instance_id = aws_service.create_ec2_instance("t2.micro")
    
    assert instance_id is not None
    mock_ec2.run_instances.assert_called_once()
```

## Integration Testing 🔄

### 1. AWS Integration
```python
# tests/integration/aws/test_resource_management.py
import pytest
from app.services import ResourceManager

@pytest.mark.integration
def test_resource_lifecycle():
    """Test complete resource lifecycle"""
    manager = ResourceManager()
    
    # Create resource
    resource_id = manager.create_resource(config)
    assert resource_id
    
    # Update resource
    updated = manager.update_resource(resource_id, new_config)
    assert updated
    
    # Delete resource
    deleted = manager.delete_resource(resource_id)
    assert deleted
```

### 2. Database Integration
```python
# tests/integration/database/test_persistence.py
import pytest
from app.models import Resource
from app.database import db

@pytest.mark.integration
async def test_resource_persistence():
    """Test resource database operations"""
    # Create
    resource = Resource(type="ec2", config={})
    await db.save(resource)
    
    # Read
    saved = await db.get(Resource, resource.id)
    assert saved.id == resource.id
    
    # Update
    resource.config = {"updated": True}
    await db.update(resource)
    
    # Delete
    await db.delete(resource)
    assert not await db.exists(Resource, resource.id)
```

## End-to-End Testing 🎯

### 1. Resource Management Flow
```python
# tests/e2e/test_resource_flow.py
import pytest
from app.client import APIClient

@pytest.mark.e2e
async def test_complete_resource_flow():
    """Test complete resource management flow"""
    client = APIClient()
    
    # Create resource
    response = await client.post("/resources", json={
        "type": "ec2",
        "config": {"instance_type": "t2.micro"}
    })
    resource_id = response.json()["resource_id"]
    
    # Monitor creation
    status = await client.get(f"/resources/{resource_id}/status")
    assert status.json()["state"] == "running"
    
    # Update resource
    update_response = await client.put(
        f"/resources/{resource_id}",
        json={"instance_type": "t2.small"}
    )
    assert update_response.status_code == 200
    
    # Delete resource
    delete_response = await client.delete(f"/resources/{resource_id}")
    assert delete_response.status_code == 204
```

## Test Configuration ⚙️

### 1. pytest Configuration
```ini
# pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = 
    --verbose
    --cov=app
    --cov-report=term-missing
```

### 2. Test Environment
```python
# tests/conftest.py
import pytest
import os

@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        "AWS_REGION": "us-east-1",
        "TEST_MODE": True,
        "DB_URL": os.getenv("TEST_DB_URL")
    }

@pytest.fixture(autouse=True)
async def setup_database():
    """Setup test database"""
    await db.connect()
    yield
    await db.disconnect()
```

## Mocking 🎭

### 1. AWS Service Mocks
```python
# tests/mocks/aws_mocks.py
class MockAWSService:
    def __init__(self):
        self.resources = {}
    
    async def create_resource(self, config):
        resource_id = str(uuid.uuid4())
        self.resources[resource_id] = config
        return resource_id
    
    async def get_resource(self, resource_id):
        return self.resources.get(resource_id)
```

### 2. Database Mocks
```python
# tests/mocks/db_mocks.py
class MockDatabase:
    def __init__(self):
        self.store = {}
    
    async def save(self, model):
        self.store[model.id] = model
        
    async def get(self, model_class, id):
        return self.store.get(id)
```

## Test Utilities 🛠️

### 1. Test Data Generators
```python
# tests/utils/generators.py
def generate_resource_config():
    """Generate test resource configuration"""
    return {
        "type": random.choice(["ec2", "s3", "rds"]),
        "config": {
            "name": f"test-resource-{uuid.uuid4()}",
            "region": "us-east-1"
        }
    }
```

### 2. Assertion Helpers
```python
# tests/utils/assertions.py
def assert_resource_valid(resource):
    """Assert resource object is valid"""
    assert resource.id is not None
    assert resource.type in ["ec2", "s3", "rds"]
    assert isinstance(resource.config, dict)
```

## Performance Testing 📊

### 1. Load Tests
```python
# tests/performance/test_load.py
import asyncio
from locust import HttpUser, task, between

class ResourceUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def create_resource(self):
        self.client.post("/resources", json={
            "type": "ec2",
            "config": {"instance_type": "t2.micro"}
        })
```

### 2. Stress Tests
```python
# tests/performance/test_stress.py
async def test_concurrent_requests():
    """Test handling of concurrent requests"""
    client = APIClient()
    tasks = [
        client.create_resource()
        for _ in range(100)
    ]
    results = await asyncio.gather(*tasks)
    assert all(r.status_code == 201 for r in results)
```

## Best Practices 📚

1. **Test Organization**
   - Clear test structure
   - Meaningful test names
   - Proper use of fixtures
   - Test isolation

2. **Test Coverage**
   - High coverage targets
   - Critical path testing
   - Edge case handling
   - Error scenarios

3. **Performance**
   - Fast test execution
   - Parallel testing
   - Resource cleanup
   - Mock external services

4. **Maintenance**
   - Regular updates
   - Documentation
   - Clean code
   - Version control
