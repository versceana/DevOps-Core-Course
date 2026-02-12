import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main_endpoint_status(client):
    """Test that main endpoint returns 200"""
    rv = client.get('/')
    assert rv.status_code == 200

def test_main_endpoint_json_structure(client):
    """Test that main endpoint contains all required fields"""
    rv = client.get('/')
    json_data = rv.get_json()
    assert 'service' in json_data
    assert 'system' in json_data
    assert 'runtime' in json_data
    assert 'request' in json_data
    assert 'endpoints' in json_data
    assert json_data['service']['name'] == 'devops-info-service'
    assert json_data['service']['framework'] == 'Flask'

def test_health_endpoint(client):
    """Test /health returns healthy status"""
    rv = client.get('/health')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'healthy'
    assert 'timestamp' in json_data
    assert 'uptime_seconds' in json_data

def test_404_error(client):
    """Test non-existent endpoint returns 404 JSON"""
    rv = client.get('/nonexistent')
    assert rv.status_code == 404
    json_data = rv.get_json()
    assert 'error' in json_data
    assert json_data['error'] == 'Not Found'
