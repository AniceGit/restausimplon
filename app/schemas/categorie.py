from pydantic import BaseModel
from typing import Optional

class CategorieCreate(BaseModel):    
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True



class CategorieRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True



class CategorieUpdate(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True



class CategorieDelete(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True