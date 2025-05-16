import pytest
from unittest.mock import patch, MagicMock
from zbyte.config import Config
from zbyte.client import Client

@pytest.fixture
def cfg():
    return Config(
        provider="stability",
        model="test-model",
        api_key="testkey",
        backend_url="https://backend.test/proof"
    )

@patch('0byte_sdk.client.requests.post')
@patch('0byte_sdk.client.requests.get')
def test_generate_image_success(mock_get, mock_post, cfg):
    gen_resp = MagicMock(status_code=200, content=b'image-bytes', headers={'Date': 'today'})
    gen_resp.raise_for_status.return_value = None
    proof_resp = MagicMock(status_code=200)
    proof_resp.raise_for_status.return_value = None
    proof_resp.json.return_value = {"transaction_id": "tx123", "image_url": "https://img.test/embedded.png"}

    mock_post.side_effect = [gen_resp, proof_resp]
    mock_get.return_value = MagicMock(content=b'emb-image')

    client = Client(cfg)
    result = client.generate_image("test")

    assert result.transaction_id == "tx123"
    assert result.image_bytes == b'emb-image'