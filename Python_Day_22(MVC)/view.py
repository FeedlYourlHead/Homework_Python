from jinja2 import Environment, FileSystemLoader
from model import Hotel

class ConsoleView:
    def display_welcome(self):
        print('-'*40)
        print('Welcome to Hotel')
        print('-'*40)

    def display_menu(self):
        print('Menu')
        print('1. All Hotels')
        print('2. Search Hotels by city')
        print('3. Book hotel')
        print('4. View Catalog')
        print('5. Exit')
        return int(input('Enter your choice: '))

    def display_hotels(self, hotels, title):
        print(f'\n---{title}---')
        if not hotels:
            print('No hotels found')
            return

        for i, h in enumerate(hotels, 1):
            print(f'[{i}] {h}')
        print('-'*15)

    def get_search_city(self):
        return input('Enter city: ')

    def get_booking_name(self):
        return input('Enter hotel name: ')

    def display_booking_result(self, success, h_name):
        if success:
            print(f'Отель {h_name} забронирован!')
        else:
            print(f'Отель {h_name} не найден или уже забронирован')

    def display_exit(self):
        print('Thank you for using this program!')

def generate_html_catalog(hotels, filename='catalog.html'):
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    try:
        template = env.get_template('hotel_template.html')
        output = template.render(hotels=hotels, title='Catalog Hotels')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
    except Exception as e:
        print('Error: ', e)