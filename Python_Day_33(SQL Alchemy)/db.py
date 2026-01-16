from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Numeric, Integer, ForeignKey
import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    registratin_date: Mapped[datetime.datetime] = mapped_column(DateTime) #TODO:Исправить, тут неверно, наверное
    orders = relationship('Order', back_populates='users')

    def __repr__(self) -> str:
        return f'id={self.id} ,username={self.username}, email={self.email}, registratin_date={self.registratin_date}'


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(30))
    price: Mapped[float] = mapped_column(Numeric())
    quantity_in_stock: Mapped[int] = mapped_column(Integer)

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id') )
    order_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String())
    users = relationship('User', back_populates='orders')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer(), ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(Integer(), ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer())
    price_at_order: Mapped[float] = mapped_column(Numeric(), ) #TODO: Сделать, чтобы цена товара на момент заказа, копировалась из Product.price

    order: Mapped['Order'] = relationship(
        back_populates='items'
    )

    product: Mapped["Product"] = relationship(
        back_populates='order_items',
        lazy='joined'
    )
