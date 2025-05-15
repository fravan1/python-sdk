class SDKError(Exception):
    """Base exception for 0byte SDK"""

class GenerationError(SDKError):
    """Raised when image generation fails"""

class ProofError(SDKError):
    """Raised when proof anchoring fails"""