from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from ..repositories.product_repository import ProductRepository
from ..schemas.category import CategoryResponse, ProductCreate, ProductResponse, ProductListResponse
from ..schemas.cart import CartItem, CartResponse
from ..repositories.category_repository import CategoryRepository
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status

rauter = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

@router.get("", response_model= ProductListResponse, status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()



@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_id(product_id)



@router.post("/category/{category_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_category(category_id)
