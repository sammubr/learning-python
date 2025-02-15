from pydantic import BaseModel, Field

class Car(BaseModel):
    description: str = Field(..., unique=True)