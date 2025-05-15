`pip install 0byte-sdk`

## Features
- Generate images via Stability AI
- Anchor proofs via 0byte Rust backend
- Returns image bytes with embedded proof and Solana txn ID

## Quick Start
```python
from 0byte_sdk import Config, Client

# Initialize
cfg = Config(
    stability_api_key="YOUR_STABILITY_KEY",
    backend_url="https://api.0byte.tech/proof",
    model="stable-diffusion-v1"
)
client = Client(cfg)

# Generate an image
result = client.generate_image(prompt="A futuristic city skyline at dawn")
print(result.transaction_id)
with open("output.png", "wb") as f:
    f.write(result.image_bytes)
```