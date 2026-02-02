from jinja2 import Environment, FileSystemLoader
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
template_env = Environment(loader=FileSystemLoader('templates'))
from db import (get_all_authors, get_author_detail, get_all_books,
                get_all_genres, setup_database, create_user, auth_user,
                get_user_by_id, add_to_read)
from http import cookies

def render_template(template_name, context={}):
    template = template_env.get_template(template_name)
    return template.render(context).encode('utf-8')

class LibraryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        uid = self.get_user_id()
        user = get_user_by_id(uid) if uid else None

        if path.startswith('/static/'):
            self.send_static(path)
            return
        content = None
        status_code = 200
        try:
            if path == '/' or path == '/authors':
                authors = get_all_authors() #прописать db
                content = render_template('authors.html',
                                          {'authors': authors,
                                                  'user': user})
            elif path.startswith('/author/'):
                try:
                    author_id = int(path.split('/')[-1])
                    author = get_author_detail(author_id)
                    if author:
                        content = render_template('author_detail.html',
                                              {'author': author,
                                                      'user': user})
                    else:
                        status_code = 404
                        content = render_template('404.html',
                                          {'message': 'Автор не найден'})
                except ValueError:
                    status_code = 400
                    content = render_template('404.html',
                                              {'message': 'Некоректный ID автора'})
            elif path == '/books':
                books = get_all_books()
                genres = get_all_genres()
                content = render_template('books.html',
                                          {'books': books,
                                                  'genres': genres,
                                                  'user': user})
            elif path == '/profile':
                if not user: self.redirect('/login'); return
                content = render_template('profile.html',
                                          {'user': user})
            elif path == '/login':
                content = render_template('login.html',
                                          {'user': user})
            elif path == '/register':
                content = render_template('register.html',
                                          {'user': user})
            elif path == '/logout':
                self.send_response(303)
                self.send_header('Set-Cookie', 'user_id=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
                self.send_header('Location', '/')
                self.end_headers()
                return

            elif path == '/book_details':
                pass
                # TODO: Дописать эндпоинт
            else:
                status_code = 404
                content = render_template('404.html',
                                          {'message': 'Страница не найдена'})
        except Exception as e:
            print(f'Ошибка при обработке запроса: {e}')
            status_code = 500
            content = render_template('500.html',
                                      {'error': str(e)})
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        if content:
            self.wfile.write(content)

    def send_static(self, path):
        file_path = path[1:]
        try:
            with open(file_path, 'rb' ) as f:
                content = f.read()
            if file_path.endswith('.css'):
                mime_types = 'text/css'
            elif file_path.endswith('.js'):
                mime_types = 'application/javascript'
            else:
                mime_types = 'application/octet-stream'

            self.send_response(200)
            self.send_header('Content-type', mime_types)
            self.send_header('Content-length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f'File not found {path}')

    def get_user_id(self):
        cookie = cookies.SimpleCookie(self.headers.get('Cookie'))
        return cookie.get('user_id').value if cookie else None

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = parse_qs(self.rfile.read(content_length).decode('utf-8'))
        path = urlparse(self.path).path
        if path == '/register':
            username = post_data['username'][0]
            password = post_data['password'][0]
            if create_user(username, password):
                self.redirect('/login')
            else:
                self.send_error(400, 'User already exists')

        elif path == '/login':
            username = post_data['username'][0]
            password = post_data['password'][0]
            user_id = auth_user(username, password)
            if user_id:
                self.send_response(303)
                self.send_header('Set-Cookie', f'user_id={user_id}; Path=/')
                self.send_header('Location', '/profile')
                self.end_headers()
            else:
                self.redirect('/login')

        elif path == '/add_read':
            user_id = self.get_user_id()
            if user_id:
                book_id = int(post_data['book_id'][0])
                add_to_read(int(user_id), book_id)
                self.redirect('/books')
            else:
                self.redirect('/login')

    def redirect(self, location):
        self.send_response(303)
        self.send_header('Location', location)
        self.end_headers()


def run_server(port=8000):
    setup_database()
    server_address = ('', port)
    httpd = HTTPServer(server_address, LibraryHandler)
    print(f'сервер запущен на http://localhost:{port}/')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
