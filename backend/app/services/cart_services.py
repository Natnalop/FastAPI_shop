from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from ..repositories.product_repository import ProductRepository
from ..schemas.category import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, ProductListResponse
from ..repositories.category_repository import CategoryRepository
from fastapi import HTTPException, status


class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def add_to_cart(self, cart_data: Dict[int, int], item: CartItemCreate) -> Dict[int, int]:
        product = self.repository.get_by_id(item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )
        if item.product_id in cart_data:
            cart_data[item.product_id] += item.quantity
        else:
            cart_data[item.product_id] = item.quantity
        return cart_data
