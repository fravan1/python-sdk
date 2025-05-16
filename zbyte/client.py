import io
import base64
import requests
from PIL import Image
from .config import Config
from .constants import PLATFORMS
from .exceptions import GenerationError, ProofError
from .utils import logger

zbyte_base = "https://zerobyte-backend.onrender.com"

class GenerationResult:
    def __init__(self, image_bytes: bytes, transaction_id: str):
        self.image_bytes = image_bytes
        self.transaction_id = transaction_id

class Client:
    def __init__(self, config: Config):
        self.cfg = config

    def generate_image(self, prompt: str) -> GenerationResult:
        if self.cfg.provider == PLATFORMS.STABILITY:
            image_bytes = self._generate_with_inference_api(prompt)
        else:
            raise GenerationError(f"Unsupported provider: {self.cfg.provider}")

        # Convert image to base64
        image_b64 = base64.b64encode(image_bytes).decode()

        metadata = {
            'image_bytes': image_b64,
            'model_name': self.cfg.model,
            'platform_name': self.cfg.platform,
            'input_token_count': 100,
            'output_token_count': 150
        }

        try:
            logger.info("Sending image to 0byte backend for proof anchoring")
            proof_resp = requests.post(zbyte_base + "/generate-proof", json=metadata)
            proof_resp.raise_for_status()
        except requests.RequestException as e:
            logger.error("Proof anchoring failed: %s", e)
            raise ProofError(e)

        txn_id = proof_resp.headers.get("X-Transaction-Id")
        if not txn_id:
            raise ProofError("Transaction ID not found in response headers")

        embedded_image_bytes = proof_resp.content  # ✅ raw bytes, not base64

        return GenerationResult(image_bytes=embedded_image_bytes, transaction_id=txn_id)

    def _generate_with_inference_api(self, prompt: str) -> bytes:
        if not self.cfg.api_key:
            raise GenerationError("Missing Hugging Face token (api_key) for inference API")

        headers = {"Authorization": f"Bearer {self.cfg.api_key}"}
        url = f"https://api-inference.huggingface.co/models/stabilityai/{self.cfg.model}"

        logger.info("Generating image using Hugging Face Inference API")

        response = requests.post(url, headers=headers, json={"inputs": prompt})
        if response.status_code != 200:
            raise GenerationError(f"Inference API failed: {response.text}")

        return response.content