import datetime
from pydantic import BaseModel

class MovementCreate(BaseModel):
    product_id: int
    quantity: int
    movement_type: str
    note: str | None = None

class MovementResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    movement_type: str
    note: str | None = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True
