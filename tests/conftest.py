import pytest
import os
import sys
from unittest.mock import MagicMock
import asyncio
import pytest_asyncio

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from beproduct import BeProduct, StyleAsync

# Shared fixtures that can be used by both sync and async tests
@pytest.fixture
def api_credentials():
    return {
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
        'refresh_token': 'test_refresh_token',
        'company_domain': 'test-company.beproduct.com'
    }

@pytest.fixture
def mock_client(api_credentials):
    client = BeProduct(**api_credentials)
    # Mock the raw_api to prevent actual API calls
    client.raw_api = MagicMock()
    return client

@pytest_asyncio.fixture
async def mock_client_async(api_credentials):
    client = BeProduct(**api_credentials)
    # Create a mock with async methods
    mock_raw_api = MagicMock()
    
    async def async_get(*args, **kwargs):
        return mock_raw_api.get(*args, **kwargs)
    
    async def async_post(*args, **kwargs):
        return mock_raw_api.post(*args, **kwargs)
    
    mock_raw_api.get = async_get
    mock_raw_api.post = async_post
    
    # Mock session for context manager tests
    mock_raw_api._session = MagicMock()
    mock_raw_api._session.closed = False
    
    async def async_close():
        mock_raw_api._session.closed = True
        mock_raw_api._session = None
    
    mock_raw_api.close = async_close
    client.raw_api = mock_raw_api
    return client

@pytest.fixture
def mock_style_data():
    return {
        'id': 'test_style_id',
        'name': 'Test Style',
        'description': 'Test Style Description'
    }

@pytest.fixture
def mock_material_data():
    return {
        'id': 'test_material_id',
        'name': 'Test Material',
        'description': 'Test Material Description'
    } 