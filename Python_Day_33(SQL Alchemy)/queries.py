from seed import DatabaseManager
from db import Product, Order, OrderItem, User



if __name__ == "__main__":
    # Смартфон <50_000
    db_manager = DatabaseManager()
    session = db_manager.get_session()

    query_smartphone = session.query(Product).filter(Product.price < 50_000, Product.category == "Смартфон").all()

    for smartphone in query_smartphone:
        print(f'id={smartphone.id}\nname={smartphone.name}\ncategory={smartphone.category}\nprice={smartphone.price}\nquantity_in_stock={smartphone.quantity_in_stock}\n')

    #  Join таблиц по email, список заказов примера ivan@yandex.ru
    email_target = 'ivan@yandex.ru'
    quer = session.query(Order).join(User).filter(User.email == email_target).all()
    for elem in quer:
        print(f'Дата заказа - {elem.order_date}, статус - {elem.status}')


    




