from random import choice

from  model import HotelCatalog
from view import ConsoleView, generate_html_catalog

class Controller:
    def __init__(self):
        self._model = HotelCatalog()
        self._view = ConsoleView()

    def run(self):
        self._view.display_welcome()
        while True:
            choice = self._view.display_menu()
            if choice == 1:
                hotels = self._model.get_all_hotels()
                self._view.display_hotels(hotels,'All Hotels')
            elif choice == 2:
                city = self._view.get_search_city()
                hotels = self._model.find_hotels_by_city(city)
                self._view.display_hotels(hotels,
                                          f'Hotels in {city}')
            elif choice == 3:
                name = self._view.get_booking_name()
                success = self._model.book_hotel(name)
                self._view.display_booking_result(success, name)

            elif choice == 4:
                all_hotels = self._model.get_all_hotels()
                generate_html_catalog(all_hotels)

            elif choice == 5:
                self._view.display_exit()
                break
            else:
                print('Invalid choice')