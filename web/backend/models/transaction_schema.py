from datetime import datetime
from enum import Enum
from typing import ParamSpec
from pydantic import BaseModel, Field, field_validator, ConfigDict

class TransactionType(str, Enum):
    CASH_IN = "CASH_IN"
    CASH_OUT = "CASH_OUT"
    DEBIT = "DEBIT"
    PAYMENT = "PAYMENT"
    TRANSFER = "TRANSFER"

class TransactionInput(BaseModel):
    amount: float = Field(..., gt=0.0)
    nameOrig: str = Field(..., pattern=r"^C\d+$")
    oldbalanceOrg: float = Field(..., ge=0.0)
    newbalanceOrig: float = Field(..., ge=0.0)
    nameDest: str = Field(..., pattern=r"^[CM]\d+$")
    oldbalanceDest: float = Field(..., ge=0.0)
    newbalanceDest: float = Field(..., ge=0.0)

    type: str = Field(...)

    step: int = Field(default_factory=lambda: datetime.now().hour)

    @field_validator('type', mode='before')
    @classmethod
    def uppercase_type(cls, v):
        if isinstance(v, str):
            return v.upper()
        return v
    class Config:
        json_schema_extra = {
                "example": {
                    "amount": 181.0,
                    "nameOrig": "C1305486145",
                    "oldbalanceOrg": 181.0,
                    "newbalanceOrig": 0.0,
                    "nameDest": "C553264065",
                    "oldbalanceDest": 0.0,
                    "newbalanceDest": 0.0,
                    "type": "TRANSFER"
                    }
                }

