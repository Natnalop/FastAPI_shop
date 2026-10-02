from pydantic import BaseModel, Field

class CategotyBase(BaseModel):
    name:str = Field(..., min_length=5, max_length=100, description="Введите название категории")
    slug:str = Field(..., min_length=5, max_length=100, description="название URL категории")

class CategoryCreate(CategotyBase):
    pass

class CategoryResponse(CategotyBase):
    id:int = Field(..., description="ID of the category")

    class Config:
        from_attributes = True

