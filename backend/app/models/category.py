from backend.app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)#Числовой идентификатор категории
    name = Column(String, unique=True, nullable = False , index=True)#Название категории:Уникальное название категории и не может быть пустым
    slug = Column(String, unique=True, nullable=False, index=True)#Техническое название категории:Уникальное техническое название категории и не может быть пустым

    products = relationship("Product", back_populates="category")#Связь с продуктами:Каждая категория может иметь множество продуктов

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}>"

