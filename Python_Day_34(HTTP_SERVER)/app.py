from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, date
import json
from jinja2 import Environment, FileSystemLoader
from database import get_db_session, Message
import os

env = Environment(loader=FileSystemLoader('templates'))

class TimeCapsuleHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Обработка GET запросов"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.show_home_page()
        elif parsed_path.path == '/create':
            self.show_create_page()
        else:
            self.send_error(404, "Страница не найдена")

    def do_POST(self):
        """Обработка POST запросов"""
        if self.path == '/create':
            self.handle_create_capsule()
        else:
            self.send_error(404, "Страница не найдена")
    
    def show_home_page(self):
        """Отображение главной страницы со списком капсул"""
        session = get_db_session()
        try:
            capsules = session.query(Message).order_by(Message.created_at.desc()).all()
            
            today = date.today()
            for capsule in capsules:
                capsule.is_unlocked = capsule.unlock_date <= today
            
            template = env.get_template('index.html')
            html_content = template.render(capsules=capsules)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Ошибка сервера: {str(e)}")
        finally:
            session.close()
    
    def show_create_page(self):
        """Отображение страницы создания капсулы"""
        tomorrow = date.today()
        min_date = tomorrow.strftime('%Y-%m-%d')
        
        template = env.get_template('create.html')
        html_content = template.render(
            min_date=min_date,
            error=None
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def handle_create_capsule(self):
        """Обработка формы создания капсулы"""
        content_length = int(self.headers['Content-Length'])
        
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(post_data)
        
        author = form_data.get('author', [''])[0].strip()
        content = form_data.get('content', [''])[0].strip()
        unlock_date_str = form_data.get('unlock_date', [''])[0]
        
        errors = []
        if not author:
            errors.append("Имя автора не может быть пустым")
        if not content:
            errors.append("Текст послания не может быть пустым")
        if not unlock_date_str:
            errors.append("Дата открытия не может быть пустой")
        
        if errors:
            tomorrow = date.today()
            min_date = tomorrow.strftime('%Y-%m-%d')
            template = env.get_template('create.html')
            html_content = template.render(
                min_date=min_date,
                error=", ".join(errors)
            )
            
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            return
        
        try:
            unlock_date = datetime.strptime(unlock_date_str, '%Y-%m-%d').date()
            today = date.today()
            
            if unlock_date <= today:
                tomorrow = date.today()
                min_date = tomorrow.strftime('%Y-%m-%d')
                template = env.get_template('create.html')
                html_content = template.render(
                    min_date=min_date,
                    error="Дата открытия должна быть в будущем"
                )
                
                self.send_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
                return
            
            session = get_db_session()
            try:
                new_capsule = Message(
                    author=author,
                    content=content,
                    unlock_date=unlock_date,
                    created_at=datetime.now()
                )
                
                session.add(new_capsule)
                session.commit()
                
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
                
            finally:
                session.close()
                
        except ValueError:
            tomorrow = date.today()
            min_date = tomorrow.strftime('%Y-%m-%d')
            template = env.get_template('create.html')
            html_content = template.render(
                min_date=min_date,
                error="Неверный формат даты"
            )
            
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
    

def run_server():
    """Запуск сервера"""
    port = 8000
    server_address = ('', port)
    
    print(f"Сервер запущен на http://localhost:{port}")
    print(f"База данных: capsules.db")
    print("Приложение 'Цифровая Капсула Времени' готово к работе!")
    print("\nДоступные страницы:")
    print(f"  • http://localhost:{port}/ - Главная страница")
    print(f"  • http://localhost:{port}/create - Создание капсулы")
    print("\nНажмите Ctrl+C для остановки сервера")
    
    httpd = HTTPServer(server_address, TimeCapsuleHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    from database import init_database
    init_database()
    
    run_server()
