from pydantic import BaseModel, Field
from typing import Optional

class CartItemBase(BaseModel):
    product_id: int = Field(..., description="ID продукта")
    quantity: int = Field(..., gt=0, description="Количество продукта")

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(CartItemBase):
    id: int = Field(..., description="Айди записи в корзине")
    product_id: int
    quantity: int

class CartItem(CartItemBase):
    product_id: int
    quantity: int
    name: str = Field(..., description="Название продукта")
    price: float = Field(..., gt=0, description="Цена продукта")
    subtotal: float = Field(..., gt=0, description="Финальная сумма записи в корзине (price * quantity)")
    image_url: Optional[str] = Field(None, description="URL изображения продукта")

class CartItemResponse(CartItem):
    items: list[CartItem] = Field(..., description="Список записей в корзине")
    total: float = Field(..., gt=0, description="Общая сумма корзины")
    items_count: int = Field(..., gt=0, description="Количество записей в корзине")

    class Config:
        from_attributes = True