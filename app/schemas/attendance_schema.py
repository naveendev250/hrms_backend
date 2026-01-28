from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Literal


class AttendanceBase(BaseModel):
    employee_id: str = Field(..., min_length=1)
    date: date
    status: Literal["Present", "Absent"]


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceResponse(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
