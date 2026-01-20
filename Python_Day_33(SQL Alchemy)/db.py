from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Numeric, Integer, ForeignKey
import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    registratin_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'id={self.id} ,username={self.username}, email={self.email}, registratin_date={self.registratin_date}'

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, default=0)

    order_items = relationship('OrderItem', back_populates='product')

    def __repr__(self) -> str:
        return f'id={self.id}, category={self.category}, price={self.price}, quantity_in_stock={self.quantity_in_stock}'

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    order_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    status: Mapped[str] = mapped_column(String, default='в обработке')
    user = relationship(
        'User',
        back_populates='orders'
    )
    items = relationship(
        'OrderItem',
        back_populates='order',
        cascade='all, delete-orphan'
    )

    def calculate_total(self):
        return sum(item.quantity * item.price_at_order for item in self.items)

    def __repr__(self) -> str:
        return f'id={self.id}, order_date={self.order_date}, status={self.status} '

class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_order: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False) 
    

    order: Mapped['Order'] = relationship(
        'Order',
        back_populates='items'
    )

    product: Mapped["Product"] = relationship(
        'Product',
        back_populates='order_items'
    )

    def __repr__(self) -> str:
        return f'id={self.id}, '
