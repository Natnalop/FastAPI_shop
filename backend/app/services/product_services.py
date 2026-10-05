from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from ..repositories.product_repository import ProductRepository
from ..schemas.category import ProductCreate, ProductResponse, ProductListResponse
from ..schemas.cart import CartItem, CartResponse
from ..repositories.category_repository import CategoryRepository
from fastapi import HTTPException, status



class ProductService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all_products(self):
        products = self.product_repository.get_all()
        products_response = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=products_response, total=len(products_response))

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        return ProductResponse.model_validate(product)

    def get_products_by_category(self, category_id: int) -> ProductListResponse:
        category = self.category_repository.get_but_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        products = self.product_repository.get_by_category(category_id)
        products_response = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=products_response, total=len(products_response))
    

    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {product_data.category_id} not found"
            )
        product = self.product_repository.create(product_data)
        return ProductResponse.model_validate(product)

    def update_product(self, product_id: int, product_data: ProductCreate) -> ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {product_data.category_id} not found"
            )
        updated_product = self.product_repository.update(product_id, product_data)
        return ProductResponse.model_validate(updated_product)

    def remove_from_cart(self, cart_data: Dict[int, int], product_id: int) -> Dict[int, int]:
        if product_id not in cart_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found in cart"
            )
        del cart_data[product_id]
        return cart_data

    def get_cart_details(self, cart_data: Dict[int, int]) -> ProductListResponse:
        if not cart_data:
            return CartResponse(items=[], total=0.0, item_count=0)
        product_ids = list(cart_data.keys())
        products = self.product_repository.get_multiple_by_ids(product_ids)
        products_dict = {product.id: product for product in products}

        cart_item = []
        total_price = 0.0
        total_items = 0
        for product_id, quantity in cart_data.items():
            if product_id in products_dict:
                product = products_dict[product_id]
                subtotal = product.price * quantity
                cart_item.append(CartItem(
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=quantity,
                    subtotal=subtotal,
                    image_url=product.image_url
                ))

                total_price += subtotal
                total_items += quantity
            return CartResponse(items=cart_item, total=round(total_price), item_count=total_items)