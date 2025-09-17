class Item:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return f"\nНазвание: {self.title}\nГод: {self.year}\n"


class Book(Item):
    def __init__(self, title, year, author, pages):
        super().__init__(title, year)
        self.author = author
        self.pages = pages

    def __str__(self):
        return (
            super().__str__()
            + f"Автор: {self.author}\nКоличество страниц: {self.pages}\n"
        )


class Magazine(Book):
    def __init__(self, title, year, author, pages, issue, publisher):
        super().__init__(title, year, author, pages)
        self.issue = issue
        self.publisher = publisher

    def __str__(self):
        return (
            super().__str__()
            + f"Номер выпуска: {self.issue}\nИздательство: {self.publisher}"
        )


def main():
    bookshelf = []
    while True:
        try:
            choice = int(
                input("""
            Выберите команду:
            1.Добавить Item
            2.Добавить Book
            3.Добавить Magazine
            4.Просмотреть содержимое
            5.Выход
            6.Просто посмотреть пример вывода
            """)
            )
            if choice not in range(1, 7):
                raise Exception
            elif choice == 1:
                title = input("Название: ")
                year = input("Год: ")
                bookshelf.append(Item(title, year))
            elif choice == 2:
                title = input("Название: ")
                year = input("Год: ")
                author = input("Автор: ")
                pages = input("Количество страниц: ")
                bookshelf.append(Book(title, year, author, pages))
            elif choice == 3:
                title = input("Название: ")
                year = input("Год: ")
                author = input("Автор: ")
                pages = input("Количество страниц: ")
                issue = input("Номер выпуска: ")
                publisher = input("Издательство: ")
                bookshelf.append(Magazine(title, year, author, pages, issue, publisher))
            elif choice == 4:
                for i in bookshelf:
                    print(i)

            elif choice == 5:
                break
            elif choice == 6:
                item_example = Item("Война и мир", 1869)
                book_example = Book(
                    "Исскуство программирования", 1962, "Дональд Кнут", 3344
                )
                magazine_example = Magazine(
                    "Журнал 'Код'", 2025, "Михаил Полянин", 500, 15, "ЯндексПрактикум"
                )
                print(item_example)
                print(book_example)
                print(magazine_example)

        except Exception:
            print("Введите корректное значение")


if __name__ == "__main__":
    main()
