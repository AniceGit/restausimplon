from pydantic import BaseModel, Field
from typing import Optional

class CategorieCreate(BaseModel):    
    name: str = Field(..., max_length=10)
    description: Optional[str] = Field(..., max_length=250)

    class Config:
        orm_mode = True



class CategorieRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True



class CategorieUpdate(BaseModel):
    name: str = Field(..., max_length=10)
    description: Optional[str] = Field(..., max_length=250)

    class Config:
        orm_mode = True



class CategorieDelete(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True