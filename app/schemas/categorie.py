from pydantic import BaseModel, Field
from typing import Optional

class CategorieCreate(BaseModel):    
    nom: str = Field(..., max_length=10)
    description: Optional[str] = Field(..., max_length=250)

    class Config:
        orm_mode = True



class CategorieRead(BaseModel):
    id: int
    nom: str
    description: Optional[str]

    class Config:
        orm_mode = True



class CategorieUpdate(BaseModel):
    id: int
    nom: str = Field(..., max_length=10)
    description: Optional[str] = Field(..., max_length=250)

    class Config:
        orm_mode = True



class CategorieDelete(BaseModel):
    id: int
    nom: str
    description: Optional[str]

    class Config:
        orm_mode = True