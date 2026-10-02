from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import Category
from ..schemas.category import CategoryCreate

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Category]:
        return self.db.query(Category).all()

    def get_but_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()


    def get_by_slug(self, slug: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.slug == slug).first()

    def create(self, category: CategoryCreate) -> Category:
        db_category = Category(name=category.name, slug=category.slug)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category