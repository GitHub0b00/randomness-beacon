import uuid
from typing import Optional
from pydantic import BaseModel, Field


# The definition of class here helps FastAPI to identify which field to be displayed in a response.
class RNG(BaseModel):
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")
    # id: object = Field(...)
    localRandomValue: str = Field(...)
    precommitmentValue: str = Field(...)
    uri: str = Field(...)
    pulseIndex: int = Field(...)
    chainIndex: int = Field(...)
    timeStamp: str = Field(...)
    listValues: list = Field(...)
    signatureValue: str = Field(...)
    outputValue: str = Field(...)
    # to be added in a new chain
    # status: str = Field(...)
