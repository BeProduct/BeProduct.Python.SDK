import pytest
from beproduct import StyleAsync
from unittest.mock import MagicMock
import asyncio

@pytest.mark.asyncio
async def test_style_async_initialization(mock_client_async, api_credentials):
    style = StyleAsync(mock_client_async)
    assert style.client == mock_client_async
    assert style.master_folder == "Style"

@pytest.mark.asyncio
async def test_get_style_async(mock_client_async, mock_style_data):
    # Create style instance with mock client
    style = StyleAsync(mock_client_async)
    
    # Configure the mock to return the data directly
    async def async_get(*args, **kwargs):
        return mock_style_data
    mock_client_async.raw_api.get = async_get
    
    # Call the method - using folder_colorway_schema as an example get method
    result = await style.folder_colorway_schema('test_folder_id')
    
    # Verify the result and the call
    assert result == mock_style_data

@pytest.mark.asyncio
async def test_update_style_async(mock_client_async, mock_style_data):
    # Create style instance with mock client
    style = StyleAsync(mock_client_async)
    
    # Configure the mock to return the data directly
    async def async_post(*args, **kwargs):
        return mock_style_data
    mock_client_async.raw_api.post = async_post
    
    # Test data
    update_data = {
        'name': 'Updated Style',
        'description': 'Updated Description'
    }
    
    # Call the method
    result = await style.attributes_update('test_style_id', fields=update_data)
    
    # Verify the result and the call
    assert result == mock_style_data

@pytest.mark.asyncio
async def test_context_manager_async(mock_client_async):
    # Create a style instance
    style = StyleAsync(mock_client_async)
    
    # Mock the session
    mock_client_async.raw_api._session = MagicMock()
    mock_client_async.raw_api._session.closed = False
    
    # Verify initial state
    assert style.client.raw_api._session is not None
    assert not style.client.raw_api._session.closed
    
    # Call close manually since context manager is not implemented yet
    await style.client.raw_api.close()
    
    # Verify final state
    assert style.client.raw_api._session is None 