class Item:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return f"Название: {self.title}\nГод: {self.year}\n"


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
    book_shell = []
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
                book_shell.append(Item(title, year))
            elif choice == 2:
                title = input("Название: ")
                year = input("Год: ")
                author = input("Автор: ")
                pages = input("Количество страниц: ")
                book_shell.append(Book(title, year, author, pages))
            elif choice == 3:
                title = input("Название: ")
                year = input("Год: ")
                author = input("Автор: ")
                pages = input("Количество страниц: ")
                issue = input("Номер выпуска: ")
                publisher = input("Издательство: ")
                book_shell.append(
                    Magazine(title, year, author, pages, issue, publisher)
                )
            elif choice == 4:
                for i in book_shell:
                    print(i)

            elif choice == 5:
                break
            elif choice == 6:
                item1 = Item("Война и мир", 1869)
                book1 = Book("Исскуство программирования", 1962, "Дональд Кнут", 3344)
                magazine1 = Magazine(
                    "Журнал 'Код'", 2025, "Михаил Полянин", 500, 15, "ЯндексПрактикум"
                )
                print(item1)
                print(book1)
                print(magazine1)

        except Exception:
            print("Введите корректное значение")


if __name__ == "__main__":
    main()
