import io
import requests
from .config import Config
from .constants import URLS
from .exceptions import GenerationError, ProofError
from .utils import logger

zero_byte_base = "https://zerobyte-backend.onrender.com"

class GenerationResult:
    def __init__(self, image_bytes: bytes, transaction_id: str):
        self.image_bytes = image_bytes
        self.transaction_id = transaction_id

class Client:
    def __init__(self, config: Config):
        self.cfg = config
        self.provider_url = self._get_provider_url()

    def _get_provider_url(self) -> str:
        base = URLS.PROVIDER_ENDPOINTS.get(self.cfg.provider)
        if not base:
            raise GenerationError(f"Unsupported provider: {self.cfg.provider}")
        return f"{base}/v1/generation/{self.cfg.model}/text-to-image"

    def generate_image(self, prompt: str) -> GenerationResult:
        headers = {"Authorization": f"Bearer {self.cfg.api_key}"}
        payload = {"text_prompts": [{"text": prompt}], "cfg_scale": 7.0}

        try:
            logger.info("Sending request to provider: %s", self.cfg.provider)
            resp = requests.post(self.provider_url, json=payload, headers=headers, timeout=self.cfg.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.error("Image generation failed: %s", e)
            raise GenerationError(e)

        image_bytes = resp.content

        # Proof anchoring
        files = { 'image': ('image.png', io.BytesIO(image_bytes), 'image/png') }
        metadata = {
            'provider': self.cfg.provider,
            'model': self.cfg.model,
            'timestamp': resp.headers.get('Date')
        }

        try:
            logger.info("Sending image to 0byte backend for proof anchoring")
            proof_resp = requests.post(self.cfg.backend_url, data=metadata, files=files, timeout=self.cfg.timeout)
            proof_resp.raise_for_status()
        except requests.RequestException as e:
            logger.error("Proof anchoring failed: %s", e)
            raise ProofError(e)

        result = proof_resp.json()
        txn_id = result.get("transaction_id")
        embedded_image_bytes = bytes(result.get("image_bytes"))

        return GenerationResult(image_bytes=embedded_image_bytes, transaction_id=txn_id)
