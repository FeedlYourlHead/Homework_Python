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


item1 = Item("Война и мир", 1869)
book1 = Book("Исскуство программирования", 1962, "Дональд Кнут", 3344)
magazine1 = Magazine("Журнал 'Код'", 2025, "Михаил Полянин", 500, 15, "ЯндексПрактикум")
print(item1)
print(book1)
print(magazine1)
