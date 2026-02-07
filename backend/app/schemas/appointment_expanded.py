from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from app.schemas.client import ClientResponse

class AppointmentWithClientResponse(BaseModel):
    id: int
    date: datetime
    description: Optional[str]
    client: ClientResponse

    model_config = {
        "from_attributes": True
    }