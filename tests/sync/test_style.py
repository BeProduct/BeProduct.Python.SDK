import pytest
from beproduct import Style

def test_style_initialization(mock_client, api_credentials):
    style = Style(mock_client)
    assert style.client == mock_client
    assert style.master_folder == "Style"

def test_get_style(mock_client, mock_style_data):
    # Create style instance with mock client
    style = Style(mock_client)
    
    # Configure the mock
    mock_client.raw_api.get.return_value = mock_style_data
    
    # Call the method - using folder_colorway_schema as an example get method
    result = style.folder_colorway_schema('test_folder_id')
    
    # Verify the result and the call
    assert result == mock_style_data
    mock_client.raw_api.get.assert_called_once_with('Style/ColorwaySchema?folderId=test_folder_id')

def test_update_style(mock_client, mock_style_data):
    # Create style instance with mock client
    style = Style(mock_client)
    
    # Configure the mock
    mock_client.raw_api.post.return_value = mock_style_data
    
    # Test data
    update_data = {
        'name': 'Updated Style',
        'description': 'Updated Description'
    }
    
    # Call the method
    result = style.attributes_update('test_style_id', fields=update_data)
    
    # Verify the result and the call
    assert result == mock_style_data
    mock_client.raw_api.post.assert_called_once() 