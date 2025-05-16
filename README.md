# 🧠 Zbyte SDK

**Zbyte** is the official Python SDK for generating AI images and anchoring cryptographic proofs to the **Solana blockchain**. It supports integration with Hugging Face inference APIs and provides a seamless backend for verifiable media.

## 🔗 What It Does

- 🖼️ Generates AI images via Hugging Face’s Stable Diffusion models  
- 🔐 Anchors a **proof of generation** to Solana using the 0Byte protocol  
- 📎 Embeds the Solana transaction ID + platform into the image metadata  
- 🛡️ Enables downstream verification of the media origin

---

## 🚀 Installation

```bash
pip install zbyte
```

✨ Quickstart
```python
from zbyte import Client, Config

config = Config(
    provider="stability",
    model="stable-diffusion-xl-base-1.0",
    api_key="your_huggingface_token",
    platform="0byte",
)

client = Client(config)

result = client.generate_image("A futuristic city at sunset")
with open("output.jpg", "wb") as f:
    f.write(result.image_bytes)

print("✅ Image verified at:", result.transaction_id)
```