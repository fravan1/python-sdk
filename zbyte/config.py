from pydantic import BaseModel, AnyUrl, Field

class Config(BaseModel):
    provider: str = Field(..., description="Image generation provider")
    model: str = Field(..., description="Model to use for generation")
    api_key: str = Field(..., description="API key for the chosen provider")
    platform: str = Field(..., description="Platform name")