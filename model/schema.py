"""Output schemas for models"""

from typing import TypedDict, Literal
from pydantic import BaseModel, Field

class ClaimCheck(BaseModel):
    """Decision on the check of sub-claim against evidence passage"""
    verdict: Literal['supported', 'refuted', 'insufficient evidence']
    confidence: float = Field(
        description='Confidence score in the range of 0.0-1.0 showing how strongly the passage supports your verdict',
    )
    grounding_sentence: str = Field(
        description='Exact sentence from the passage that supports your verdict. None if it is insufficient evidence',
        default=None
    )

class SubClaim(BaseModel):
    """Extracted sub-claims"""
    sub_claims: list[str] = Field(description='List of sub-claims from a given claim')