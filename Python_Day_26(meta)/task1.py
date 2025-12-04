
class DocstringEnforcer(type):
    def __new__(cls, name, bases, namespace):
        doc = namespace.get('__doc__')
        if doc == "" or doc == None or doc.isspace():
            raise TypeError('Класс должен иметь документацию')
        print(f"Класс {name} был успешно создан")
        return super().__new__(cls, name, bases, namespace)



class DocumentedClass(metaclass=DocstringEnforcer):
    """Какая-то документация"""
    pass


class UndocumentedClass(metaclass=DocstringEnforcer): #Класс без документации
    """                    """

    pass



if __name__ == '__main__':
    try:
        class1 = DocumentedClass()
        class2 = UndocumentedClass()
    except TypeError:
        pass

