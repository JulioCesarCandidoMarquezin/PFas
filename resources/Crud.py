from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Time, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

import bcrypt
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:3306/site_consciencia_negra"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Base = declarative_base()

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    password = Column(String(60))
    salt = Column(String(60))

class Comment(db.Model):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type_id = Column(Integer, nullable=False)
    type = Column(String(20), CheckConstraint("type IN ('photos', 'movies', 'events')"), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now())

    user = relationship('User', backref='comments')

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(Text, nullable=False)
    title = Column(String(100), unique=True, nullable=False)
    sinopse = Column(Text)
    date = Column(Date)
    duration = Column(Time)
    classification = Column(Integer)

class Event(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    description = Column(String(100))
    date = Column(Date)
    local = Column(String(100))

class Photo(db.Model):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(255), nullable=False)
    caption = Column(Text)
    date = Column(Date)

# Configuração do banco de dados
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/site_consciencia_negra"
engine = create_engine(DATABASE_URL)

# Cria as tabelas no banco de dados
Base.metadata.create_all(engine)

# Configuração da conexão com o banco de dados (substitua pelos seus próprios valores)
db_config = {
    'host': 'localhost',
    'database': 'site_consciencia_negra',
    'user': 'root',
    'password': 'root'
}

def get_database_connection():
    return mysql.connector.connect(**db_config)

# Auth #

# Register
@app.route('/auth/register', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')

    try:
        with get_database_connection() as conn, conn.cursor() as cursor:
            # Gera um salt aleatório
            salt = bcrypt.gensalt()
            
            # Gera o hash da senha utilizando o salt
            hashed_senha = bcrypt.hashpw(password.encode('utf-8'), salt)

            query = "SELECT name FROM users WHERE name = %s"
            cursor.execute(query, (name,))
            existing_user = cursor.fetchone()
            if existing_user:
                return make_response(jsonify({"message": "Nome de usuário já cadastrado"}), 409)

            query = "INSERT INTO users (name, password, salt) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, hashed_senha, salt))
            conn.commit()

        return make_response(jsonify({"message": "Cadastro bem-sucedido"}), 200)

    except mysql.connector.Error as e:
        return make_response(jsonify({"message": "Cadastro mal-sucedido"}), 500)

# Login
@app.route('/auth/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')

    try:
        with get_database_connection() as conn, conn.cursor() as cursor:
            query = "SELECT * FROM users WHERE name = %s"
            cursor.execute(query, (name,))
            user = cursor.fetchone()

        if user:
            stored_hashed_password = user[2]  # Índice correspondente à coluna 'password' na tabela

            # Verifica se as senhas coincidem
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                # Login bem-sucedido
                return make_response(jsonify({"message": "Login bem-sucedido"}), 200)

        # Login falhou
        return make_response(jsonify({"message": "Nome de usuário ou senha incorretos"}), 401)

    except mysql.connector.Error as e:
        return make_response(jsonify({"message": f"Erro ao processar login"}), 500)


# Serization #

def serialize_comment(comment):
    return {
        'id': comment.id,
        'user_id': comment.user_id,
        'type_id': comment.type_id,
        'type': comment.type,
        'text': comment.text,
        'date': comment.date.strftime('%d-%m-%Y %H:%M:%S'),  # Formato de data e hora desejado
    }

def serialize_event(event):
    return {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.strftime('%d-%m-%Y'),  # Converte a data para string no formato desejado
        'local': event.local
    }

def serialize_movie(movie):
    return {
        'id': movie.id,
        'image_url': movie.image_url,
        'title': movie.title,
        'sinopse': movie.sinopse,
        'date': movie.date.strftime('%d-%m-%Y'),  # Converte a data para string no formato desejado
        'duration': str(movie.duration),  # Converte a duração para string ou ajuste conforme necessário
        'classification': movie.classification
    }

# Movies #

# Index
@app.route('/api/movies', methods=['GET'])
def get_movies():
    try:
        movies = Movie.query.all()

        # Converter datetime e timedelta para strings antes de enviar a resposta
        serialized_movies = [serialize_movie(movie) for movie in movies]

        return make_response(jsonify({'movies': serialized_movies}), 200)

    except Exception as e:
        return make_response(jsonify({"message": "Erro ao obter filmes"}), 500)

# Create
@app.route('/api/movies', methods=['POST'])
def add_movie():
    try:
        data = request.get_json()
        new_movie = Movie(
            title=data['title'],
            sinopse=data['sinopse'],
            date=data['date'],
            duration=data['duration'],
            classification=data['classification'],
            image_url=data['image_url']
        )

        # Adicione lógica para inserir no banco de dados
        db.session.add(new_movie)
        db.session.commit()

        return make_response(jsonify({'message': 'Filme adicionado com sucesso', 'movie': serialize_movie(new_movie)}), 201)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao adicionar filme'}), 500)

#Get By Id
@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    try:
        movie = Movie.query.get(movie_id)

        if movie:
            return make_response(jsonify({'movie': serialize_movie(movie)}), 200)

        return make_response(jsonify({'message': 'Filme não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao obter filme'}), 500)

# Get By Name
@app.route('/api/movies/name/<string:movie_name>', methods=['GET'])
def get_movie_by_name(movie_name):
    try:
        movie = Movie.query.filter_by(title=movie_name).first()

        if movie:
            return make_response(jsonify({'movie': serialize_movie(movie)}), 200)

        return make_response(jsonify({'message': 'Filme não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao obter filme'}), 500)

# Update By Id
@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    try:
        movie = Movie.query.get(movie_id)

        if movie:
            data = request.get_json()
            movie.title = data.get('title', movie.title)
            movie.sinopse = data.get('sinopse', movie.sinopse)
            movie.date = data.get('date', movie.date)
            movie.duration = data.get('duration', movie.duration)
            movie.classification = data.get('classification', movie.classification)
            movie.image_url = data.get('image_url', movie.image_url)

            db.session.commit()

            return make_response(jsonify({'message': 'Filme atualizado com sucesso', 'movie': serialize_movie(movie)}), 200)

        return make_response(jsonify({'message': 'Filme não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao atualizar filme'}), 500)

# Delete By Id
@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie_by_id(movie_id):
    try:
        movie = Movie.query.get(movie_id)

        if movie:
            db.session.delete(movie)
            db.session.commit()

            return make_response(jsonify({'message': 'Filme deletado com sucesso'}), 200)

        return make_response(jsonify({'message': 'Filme não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao deletar filme'}), 500)

# Delete By Date
@app.route('/api/movies/<string:movie_date>', methods=['DELETE'])
def delete_movie_by_date(movie_date):
    try:
        movies = Movie.query.filter_by(date=movie_date).all()

        if movies:
            for movie in movies:
                db.session.delete(movie)
            db.session.commit()

            return make_response(jsonify({'message': 'Filmes deletados com sucesso'}), 200)

        return make_response(jsonify({'message': 'Filmes não encontrados'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao deletar filme'}), 500)

# Comments #

# Index
@app.route('/api/comments', methods=['GET'])
def get_comments():
    try:
        comments = Comment.query.all()
        comments = [serialize_comment(comment) for comment in comments]
        return make_response(jsonify({'comments': [comment for comment in comments]}), 200)

    except Exception as e:
        return make_response(jsonify({"message": "Erro ao obter comentários"}), 500)

# Create
@app.route('/api/comments', methods=['POST'])
def add_comment():
    try:
        data = request.get_json()
        new_comment = Comment(
            user_id=data['user_id'],
            type_id=data['type_id'],
            type=data['type'],
            text=data['text'],
            date=data['date']
        )
        db.session.add(new_comment)
        db.session.commit()

        new_comment = serialize_comment(new_comment)
        return make_response(jsonify({'message': 'Comentário adicionado com sucesso', 'comment': new_comment}), 201)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao adicionar comentário', 'error': e}), 500)

# Get By User_Id
@app.route('/api/comments/<int:user_id>', methods=['GET'])
def get_comments_by_user_id(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            comments = user.comments
            comments = [serialize_comment(comment) for comment in comments]
            return make_response(jsonify({'comments': [comment for comment in comments]}), 200)
        return make_response(jsonify({'message': 'Comentários não encontrados'}), 404)

    except Exception as e:
        return make_response(jsonify({"message": "Erro ao obter comentários"}), 500)

# Get By User_Name
@app.route('/api/comments/user/<string:user_name>', methods=['GET'])
def get_comments_by_user_name(user_name):
    try:
        user = User.query.filter_by(name=user_name).first()
        if user:
            comments = user.comments
            comments = [serialize_comment(comment) for comment in comments]
            return make_response(jsonify({'comments': [comment for comment in comments]}), 200)
        return make_response(jsonify({'message': 'Comentários não encontrados'}), 404)

    except Exception as e:
        return make_response(jsonify({"message": "Erro ao obter comentários"}), 500)

# Get By Type
@app.route('/api/comments/type/<string:type>', methods=['GET'])
def get_comments_by_type(type):
    if type not in ('photos', 'movies', 'events'):
        return make_response(jsonify({'message': 'Tipo de comentário inválido'}), 400)
    try:
        comments = Comment.query.filter_by(type=type).all()
        comments = [serialize_comment(comment) for comment in comments]
        if comments:
            return make_response(jsonify({'comments': comments}), 200)
        else:
            return make_response(jsonify({'message': 'Comentários não encontrados'}), 404)

    except Exception as e:
        return make_response(jsonify({"message": "Erro ao obter comentários"}), 500)

# Get By Type_Id
@app.route('/api/comments/<string:type>/<int:type_id>', methods=['GET'])
def get_comments_by_type_id(type, type_id):
    try:
        comments = Comment.query.filter_by(type=type, type_id=type_id).all()
        comments = [serialize_comment(comment) for comment in comments]
        return make_response(jsonify({'comments': [comment for comment in comments]}), 200) if comments else jsonify({'message': 'Comentários não encontrados'}), 404

    except Exception as e:
        return make_response(jsonify({"message": "Erro ao obter comentários"}), 500)

# Update By Id
@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)
        if comment:
            data = request.get_json()
            comment.user_id = data['user_id']
            comment.type_id = data['type_id']
            comment.type = data['type']
            comment.text = data['text']
            comment.date = data['date']
            db.session.commit()

            comment = serialize_comment(comment)
            return make_response(jsonify({'message': 'Comentário atualizado com sucesso', 'comment': comment}), 200)
        return make_response(jsonify({'message': 'Comentário não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao atualizar o comentário'}), 500)

# Delete By Id
@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return make_response(jsonify({'message': 'Comentário deletado com sucesso'}), 200)
        return make_response(jsonify({'message': 'Comentário não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao deletar o comentário'}), 500)

# Delete By User_id
@app.route('/api/comments/user/<int:user_id>', methods=['DELETE'])
def delete_comment_by_user_id(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            comments = user.comments
            for comment in comments:
                db.session.delete(comment)
            db.session.commit()
            return make_response(jsonify({'message': 'Comentários deletados com sucesso'}), 200)
        return make_response(jsonify({'message': 'Usuário não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao deletar os comentários'}), 500)

# Delete By Type
@app.route('/api/comments/type/<string:type>', methods=['DELETE'])
def delete_comment_by_type(type):
    try:
        comments = Comment.query.filter_by(type=type).all()
        if comments:
            for comment in comments:
                db.session.delete(comment)
            db.session.commit()
            return make_response(jsonify({'message': 'Comentários deletados com sucesso'}), 200)
        else:
            return make_response(jsonify({'message': 'Comentários não encontrados'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao deletar os comentários'}), 500)

# Delete By Type_Id
@app.route('/api/comments/type/<string:type>/<int:type_id>', methods=['DELETE'])
def delete_comment_by_type_id(type, type_id):
    try:
        comments = Comment.query.filter_by(type=type, type_id=type_id).all()
        if comments:
            for comment in comments:
                db.session.delete(comment)
            db.session.commit()
            return make_response(jsonify({'message': 'Comentários deletados com sucesso'}), 200)
        return make_response(jsonify({'message': 'Comentários não encontrados'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao deletar os comentários'}), 500)

# Events #

# Index
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events = Event.query.all()
        events_list = [serialize_event(event) for event in events]
        return make_response(jsonify({'events': events_list}), 200)

    except Exception as e:
        return make_response(jsonify({"message": "Erro ao obter eventos"}), 500)

# Create
@app.route('/api/events', methods=['POST'])
def add_event():
    try:
        data = request.get_json()
        new_event = Event(title=data['title'], description=data['description'], date=data['date'], local=data['local'])
        db.session.add(new_event)
        db.session.commit()

        new_event = serialize_event(new_event)
        new_event = serialize_event(new_event)
        return make_response(jsonify({'message': 'Evento adicionado com sucesso', 'event': new_event}), 201)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao adicionar evento'}), 500)

# Get By Id
@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)

    if event:
        event = serialize_event(event)
        return jsonify({'event': event})
    
    return make_response(jsonify({'message': 'Evento não encontrado'}), 404)

# Get By Name
@app.route('/api/events/name/<string:event_name>', methods=['GET'])
def get_event_by_name(event_name):
    event = Event.query.filter_by(title=event_name).first()

    if event:
        event = serialize_event(event)
        return make_response(jsonify({'event': event}))
    
    return make_response(jsonify({'message': 'Evento não encontrado'}), 404)

# Get By Date
@app.route('/api/events/date/<string:date>', methods=['GET'])
def get_events_by_date(date):
    events = Event.query.filter_by(date=date).all()

    if events:
        events_list = [serialize_event(event) for event in events]
        return make_response(jsonify({'events': events_list}), 200)
    
    return make_response(jsonify({'message': 'Nenhum evento para essa data'}), 404)

# Get By Local
@app.route('/api/events/local/<string:local>', methods=['GET'])
def get_events_by_local(local):
    events = Event.query.filter_by(local=local).all()

    if events:
        events_list = [serialize_event(event) for event in events]
        return make_response(jsonify({'events': events_list}), 200)
    
    return make_response(jsonify({'message': 'Eventos não encontrados'}), 404)

# Get By Date And Local
@app.route('/api/events/<string:date>/<string:local>', methods=['GET'])
def get_events_by_date_and_local(date, local):
    events = Event.query.filter_by(date=date, local=local).all()

    if events:
        events_list = [serialize_event(event) for event in events]
        return make_response(jsonify({'events': events_list}), 200)
    
    return make_response(jsonify({'message': 'Eventos não encontrados'}), 404)

# Update By Id
@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        event = Event.query.get(event_id)

        if event:
            data = request.get_json()
            event.title = data.get('title', event.title)
            event.description = data.get('description', event.description)
            event.date = data.get('date', event.date)
            event.local = data.get('local', event.local)
            db.session.commit()

            event = serialize_event(event)
            return make_response(jsonify({'message': 'Evento atualizado com sucesso', 'event': event}), 200)
        
        return make_response(jsonify({'message': 'Evento não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao atualizar o evento'}), 500)

# Delete By Id
@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        event = Event.query.get(event_id)

        if event:
            db.session.delete(event)
            db.session.commit()

            event = serialize_event(event)
            return make_response(jsonify({'message': 'Evento deletado com sucesso'}), 200)
        
        return make_response(jsonify({'message': 'Evento não encontrado'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao deletar o evento'}), 500)

# Photos #

# Index
@app.route('/api/photos', methods=['GET'])
def get_photos():
    try:
        photos = Photo.query.all()
        photos_list = [photo.__dict__ for photo in photos]
        return make_response(jsonify({'photos': photos_list}), 200)

    except Exception as e:
        return make_response(jsonify({"message": "Erro ao obter fotos"}), 500)

# Create
@app.route('/api/photos', methods=['POST'])
def add_photo():
    try:
        data = request.get_json()
        new_photo = Photo(image_url=data['image_url'], caption=data['caption'], date=data['date'])
        db.session.add(new_photo)
        db.session.commit()

        return make_response(jsonify({'message': 'Foto adicionada com sucesso', 'photo': new_photo.__dict__}), 201)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao adicionar foto'}), 500)
    
#Get By Id
@app.route('/api/photos/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
    photo = Photo.query.get(photo_id)

    if photo:
        return make_response(jsonify({'photo': photo.__dict__}), 200)
    
    return make_response(jsonify({'message': 'Foto não encontrada'}), 404)

# Get By Date
@app.route('/api/photos/date/<string:date>', methods=['GET'])
def get_photos_by_date(date):
    photos = Photo.query.filter_by(date=date).all()

    if photos:
        photos_list = [photo.__dict__ for photo in photos]
        return make_response(jsonify({'photos': photos_list}), 200)
    
    return make_response(jsonify({'message': 'Fotos não encontradas'}), 404)

# Update By Id
@app.route('/api/photos/<int:photo_id>', methods=['PUT'])
def update_photo(photo_id):
    try:
        photo = Photo.query.get(photo_id)

        if photo:
            data = request.get_json()
            photo.image_url = data.get('image_url', photo.image_url)
            photo.caption = data.get('caption', photo.caption)
            photo.date = data.get('date', photo.date)
            db.session.commit()

            return make_response(jsonify({'message': 'Foto atualizada com sucesso', 'photo': photo.__dict__}), 200)
        
        return make_response(jsonify({'message': 'Foto não encontrada'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao atualizar a foto'}), 500)

# Delete By Id
@app.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    try:
        photo = Photo.query.get(photo_id)

        if photo:
            db.session.delete(photo)
            db.session.commit()

            return make_response(jsonify({'message': 'Foto deletada com sucesso'}), 200)
        
        return make_response(jsonify({'message': 'Foto não encontrada'}), 404)

    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao deletar a foto'}), 500)


if __name__ == '__main__':
    app.run(debug=True)