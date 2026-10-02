from pydantic import BaseModel, Field
from backend.app.schemas.category import CategoryResponse
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length= 200, description="Введите название продукта")
    description: Optional[str] = Field(None , max_length=1000, description="Введите описание продукта")
    price: float = Field(..., gt=0, description="Введите цену продукта")
    category_id: int = Field(..., description="ID категории продукта")
    image_id: Optional[str] = Field(None, description="URL изображения продукта")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int = Field(..., description="Айди продукта")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_id: Optional[str]
    category: CategoryResponse = Field(..., description="Категория продукта")
    created_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse] = Field(..., description="Список продуктов")
    total: int = Field(..., description="Общее количество продуктов")