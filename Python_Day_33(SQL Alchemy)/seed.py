from db import Base, User, Product, Order, OrderItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager:

    def __init__(self, database_url='sqlite:///electronics_store.db') -> None:
        self.engine = create_engine(database_url, echo=True)
        self.session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        print('Таблицы созданы!')

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
        print('Таблицы удалены!')

    def get_session(self):
        return self.session()
    

if __name__ == '__main__':
    db_manager = DatabaseManager()
    db_manager.create_tables()

    session = db_manager.get_session()

    try:
        user1 = User(username='Ivan_Ivanov', email='ivan@yandex.ru')
        user2 = User(username='Petr_Petrov', email='petr@yandex.ru')
        user3 = User(username='Andrey_Andreev', email='andrey@yandex.ru')
        user4 = User(username='Denis_Denisov', email='denis@yandex.ru')
        user5 = User(username='Maxim_Maximov', email='maxim@yandex.ru')

        session.add_all([user1, user2, user3, user4, user5])
        session.commit()

        products = [
            Product(
                name="Iphone 15 Pro",
                category='Смартфон',
                price=129999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="Samsung Galaxy",
                category='Смартфон',
                price=89999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="Poco X3",
                category='Смартфон',
                price=50999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="Samsung TV",
                category='Телевизор',
                price=79999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="Huawei TV",
                category='Телевизор',
                price=89999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="Apple TV",
                category='Телевизор',
                price=119999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="Samsung Notebook",
                category='Ноутбук',
                price=59999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="MacBook",
                category='Ноутбук',
                price=159999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="Huawei Notebook",
                category='Ноутбук',
                price=39999.99,
                quantity_in_stock=50
            ), 
            Product(
                name="LG Notebook",
                category='Ноутбук',
                price=69999.99,
                quantity_in_stock=50
            )
        ]
        session.add_all(products)
        session.commit()

        order1 = Order(
            user_id=user1.id,
            status='в обработке'
        )
        order2 = Order(
            user_id=user2.id,
            status='в обработке'
        )
        order3 = Order(
            user_id=user3.id,
            status='в обработке'
        )
        order4 = Order(
            user_id=user4.id,
            status='в обработке'
        )
        order5 = Order(
            user_id=user5.id,
            status='в обработке'
        )
        
        session.add_all([order1, order2, order3, order4, order5])
        session.flush()

        order_items = [
            OrderItem(
                order_id=order1.id,
                product_id=products[0].id,
                quantity=1,
                price_at_order=products[0].price
            ),
            OrderItem(
                order_id=order1.id,
                product_id=products[3].id,
                quantity=1,
                price_at_order=products[3].price
            ),
            OrderItem(
                order_id=order2.id,
                product_id=products[1].id,
                quantity=1,
                price_at_order=products[1].price
            ),
            OrderItem(
                order_id=order2.id,
                product_id=products[6].id,
                quantity=1,
                price_at_order=products[6].price
            ),
            OrderItem(
                order_id=order3.id,
                product_id=products[3].id,
                quantity=1,
                price_at_order=products[3].price
            ),
            OrderItem(
                order_id=order3.id,
                product_id=products[4].id,
                quantity=1,
                price_at_order=products[4].price
            ),
            OrderItem(
                order_id=order4.id,
                product_id=products[8].id,
                quantity=1,
                price_at_order=products[8].price
            ),
            OrderItem(
                order_id=order4.id,
                product_id=products[5].id,
                quantity=1,
                price_at_order=products[5].price
            ),
            OrderItem(
                order_id=order5.id,
                product_id=products[2].id,
                quantity=1,
                price_at_order=products[2].price
            ),
            OrderItem(
                order_id=order5.id,
                product_id=products[7].id,
                quantity=1,
                price_at_order=products[7].price
            )
        ]

        session.add_all(order_items)

        products[0].quantity_in_stock -= 1
        products[3].quantity_in_stock -= 1
        products[1].quantity_in_stock -= 1
        products[6].quantity_in_stock -= 1
        products[3].quantity_in_stock -= 1
        products[4].quantity_in_stock -= 1
        products[8].quantity_in_stock -= 1
        products[5].quantity_in_stock -= 1
        products[2].quantity_in_stock -= 1
        products[7].quantity_in_stock -= 1

        session.commit()


    except Exception:
        pass





