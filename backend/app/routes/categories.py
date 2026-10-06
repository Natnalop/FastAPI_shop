from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from ..repositories.product_repository import ProductRepository
from ..schemas.category import CategoryResponse, ProductCreate, ProductResponse, ProductListResponse
from ..schemas.cart import CartItem, CartResponse
from ..repositories.category_repository import CategoryRepository
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
)


@router.get("", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_category_by_id(category_id)

