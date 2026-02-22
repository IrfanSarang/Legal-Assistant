from pydantic import BaseModel, Field
from typing import List, Dict, Any


# ===============================
# REQUEST SCHEMA
# ===============================

class ContractAnalysisRequest(BaseModel):
    """
    Input schema for contract analysis.
    """

    contract_text: str = Field(
        ...,
        min_length=10,
        description="Full contract text to be analyzed."
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of relevant law sections to retrieve."
    )


# ===============================
# RESPONSE SCHEMA
# ===============================

class ContractAnalysisResponse(BaseModel):
    """
    Output schema for contract analysis.
    """

    analysis: str = Field(
        ...,
        description="LLM generated legal analysis."
    )

    relevant_law_sections: List[Dict[str, Any]] = Field(
        ...,
        description="Retrieved Indian Contract Act sections used for analysis."
    )