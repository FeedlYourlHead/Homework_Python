from sqlalchemy import (create_engine,
                        String, Integer,
                        ForeignKey, Table, Column, select, Text)
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column, relationship, Session,
                            selectinload)

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    # id = Column(Integer(), )
    name: Mapped[str] = mapped_column(String(30), nullable=False) # unique=True
    books: Mapped[list['Book']] = relationship(back_populates='author',
                                               cascade='all, delete-orphan') #save-update
    bio: Mapped['AuthorBio'] = relationship(back_populates='author',
                                            cascade='all, delete-orphan',
                                            uselist=False)
    def __repr__(self):
        return f'Author: id={self.id}, name={self.name}'

# МНОГИЕ-КО-МНОГИМ

book_genre_association = Table(
    'book_genre', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id',
                                          ondelete='CASCADE'),
           primary_key=True),
           Column('genre_id', Integer, ForeignKey('genres.id',
                                                  ondelete='CASCADE'),
                  primary_key=True)
)



# ОДИН-КО-МНОГИМ
class Book(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id',
                                                      ondelete='CASCADE')) #SET NULL | RESTRICT
    author: Mapped['Author'] = relationship(back_populates='books',
                                            lazy='joined')
    genres: Mapped[list['Genre']] = relationship(
        'Genre', secondary=book_genre_association,
        back_populates='books', lazy='select'
    )
    description: Mapped[str] = mapped_column(Text) 
    img: Mapped[str] = mapped_column(Text) 

    # back_populates - название атрибута связи (двусторонняя связь)
    # ForeignKey через таблицы обращаемся к атрибуту (id)
    # в Mapped указываем название модели(класса)

    def __repr__(self):
        return f'Book: id={self.id}, name={self.name}, author_id={self.author_id}'

# ОДИН-К-ОДНОМУ
class AuthorBio(Base):
    __tablename__ = 'author_bios'
    id: Mapped[int] = mapped_column(primary_key=True)
    bio_text: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'),
                                           unique=True, nullable=False)
    author: Mapped['Author'] = relationship(
        back_populates='bio', lazy='joined'
    )
    def __repr__(self):
        return f'AuthorBio: id={self.id}, author_id={self.author_id}'



class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    books: Mapped[list['Book']] = relationship(secondary=book_genre_association,
        back_populates='genres',
        lazy='select'
    )


user_read_books = Table(
    'user_read_books', Base.metadata,
    Column('user_id', Integer,
           ForeignKey('users.id', ondelete='CASCADE'),
                primary_key=True),
        Column('book_id', Integer,
           ForeignKey('books.id', ondelete='CASCADE'),
                primary_key=True)
            )
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    read_books: Mapped[list['Book']] = relationship(secondary=user_read_books)

DB_URL = 'sqlite:///library.db'
engine = create_engine(DB_URL, echo=False)

def setup_database():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        if session.query(Author).count()==0:
            a1 = Author(name='Дж. К. Роулинг')
            ab1 = AuthorBio(bio_text='Британская писательница...',
                            author=a1)
            a2 = Author(name='Агата Кристи')
            ab2 = AuthorBio(bio_text='Мастер детективного жанра...',
                            author=a2)
            g1, g2, g3 = Genre(name='Роман'), Genre(name='Фантастика'), Genre(name='Детектив')
            b1 = Book(name='Гарри Поттер и филосовский камень', author=a1, description='Сюжет строится вокруг главного героя, сироты Гарри Поттера, который узнаёт, что он волшебник в его одиннадцатый день рождения. Обучаясь в школе чародейства и волшебства «Хогвартс», он заводит себе близких друзей, Рона Уизли и Гермиону Грейнджер, с помощью которых останавливает попытку возвращения злого волшебника Волан-де-Морта, убившего родителей Гарри, когда ему было всего шесть месяцев.', img='https://upload.wikimedia.org/wikipedia/ru/d/d2/Обложка_первого_издания_романа_Гарри_Поттер_и_философский_камень.jpg')
            b1.genres.extend([g1, g2])
            b2 = Book(name='Убийство в Восточном экспрессе', author=a2, description='Иерусалим, 1934 год. Знаменитого бельгийского сыщика Эркюля Пуаро (Кеннет Брана) просят раскрыть загадочное преступление. Перед тем как провозгласить итоги расследования, Пуаро пытается позавтракать. Ему доставляют яйца, но Пуаро недоволен тем, что они неодинакового размера. В конечном итоге он отказывается от завтрака и отправляется к Стене Плача. Из Храма Гроба Господня похитили реликвию, в краже подозревают раввина, имама и священника. Преступник оставил улики в виде следов дорогой обуви. Бедные служители культа не могут позволить себе такую, зато подобные ботинки носит главный инспектор полиции, а ему выгодно разжигать межконфессиональную рознь. При обыске в его доме найдена похищенная ценность. Преступник пытается бежать, но при помощи Пуаро его удаётся схватить.', img='https://upload.wikimedia.org/wikipedia/ru/1/16/Убийство_в_«Восточном_экспрессе».jpg')
            b2.genres.append(g3)
            session.add_all([a1, a2, ab1, ab2, g1, g2, g3, b1, b2])
            session.commit()

    print('База данных и таблицы созданы ')



#  get_all_books, get_all_genres
def get_all_authors():
    with Session(engine) as session:
        select_authors = select(Author).order_by(Author.name)
        authors = session.scalars(select_authors).all()
        return authors

def get_author_detail(a_id):
    with Session(engine) as session:
        sab = (
            select(Author)
            .options(selectinload(Author.bio), selectinload(Author.books))
            .where(Author.id == a_id)
        )
        # select_details = select(Author).where(Author.id == a_id).limit(1)
        author = session.scalars(sab).first()
        return author

def get_all_books():
    with Session(engine) as session:
        sbg = select(Book).options(selectinload(Book.genres)).order_by(Book.name)
        # select_books = select(Book).order_by(Book.name)
        books  = session.scalars(sbg).all()
        return books

def get_all_genres():
    with Session(engine) as session:
        select_genres = select(Genre).order_by(Genre.name)
        genres  = session.scalars(select_genres).all()
        return genres

def create_user(username, password):
    with Session(engine) as session:
        user = User(username=username, password=password)
        session.add(user)
        try:
            session.commit()
            return True
        except:
            return False

def auth_user(username, password):
    with Session(engine) as session:
        user =session.query(User).filter_by(username=username, password=password).first() #scalar
        return user.id if user else None

def get_user_by_id(user_id):
    with Session(engine) as session:
        return session.query(User).options(selectinload(User.read_books)).filter_by(id=user_id).first()

def add_to_read(user_id, book_id):
    with Session(engine) as session:
        user = session.query(User).filter_by(id=user_id).first()
        book = session.query(Book).filter_by(id=book_id).first()
        if user and book and book not in user.read_books:
            user.read_books.append(book)
            session.commit()

def get_book_detail(book_id):
    with Session(engine) as session:
        return session.query(Book).options(selectinload(Book.genres), selectinload(Book.author)).filter_by(id=book_id).first()
