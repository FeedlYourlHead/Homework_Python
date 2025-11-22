
class Model:
    pass

class Controller:
    def __init__(self):
        self._model = Model()
        self._view = View()
    def run(self):
        self._view.display_welcome()
        choice = self._view.display_menu()

        if choice == 1:
            pass
            # Создать файл 
        elif choice == 2:
            pass
            # Редактировать файл

        elif choice == 3:
            pass#WARNING:Исправить позже
            #Другое
class View:
    def display_welcome(self):
        print('-'*20)
        print('Welcome to TextEditor')
        print('-'*20)

    def display_menu(self):
        print('Menu')
        print('1.Add note')
        print('2. Edit note')
        print('3. Else') #WARNING:Исправить позже

    def display_exit(self):
        print('-'*20)
        print('Thank You for using this program')
        print('-'*20)


def main():
    app = Controller()
    app.run()

if __name__ == '__main__':
    main()

