from flask import Flask, jsonify, g
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, marshal, request
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
import json
auth = HTTPBasicAuth()



app = Flask(__name__)
api = Api(app)

#Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Creation of Song Table


class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(500), nullable=False)
	password = db.Column(db.String(500), nullable=False)

	def hash_password(self, password):
		#print(self.password_hash)
		print(password)
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		print("I am in verify method")
		print(password)
		return pwd_context.verify(password, self.password)

class Admin(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(500), nullable=False)
	password = db.Column(db.String(500), nullable=False)

	def hash_password(self, password):
		#print(self.password_hash)
		print(password)
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		print(password)
		return pwd_context.verify(password, self.password)

genres_association = db.Table('genre_movies',
	db.Column('genre_id',db.Integer,db.ForeignKey('genre.id')),
	db.Column('movie_id',db.Integer,db.ForeignKey('movie.id')))
	#PrimaryKeyConstraint('genre_id', 'movie_id'))

class Movie(db.Model):
	print(" I am in model class")
	id = db.Column(db.Integer, primary_key=True)
	popularity = db.Column(db.Float, nullable=False)
	director_id = db.Column(db.Integer, db.ForeignKey('director.id') )
	#genre_id = db.Column(db.Integer, db.ForeignKey('genre.id') )
	imdb_score = db.Column(db.Float, nullable=False)
	name = db.Column(db.String(200), nullable=False)
	director = db.relationship('Director' , back_populates='movies_dir', lazy = 'select' )
	genre = db.relationship('Genre',secondary='genre_movies',back_populates='movies' , lazy = 'select')

	def asdict(self):
		list1 = []
		for gen in self.genre:
			list1.append(gen.genre)
		#str1 = str(list1)
		return {'id': self.id, '99popularity': self.popularity, 'director': self.director.name , 'genre': list1, 'imdb_score': self.imdb_score, 'name': self.name }

class Genre(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	genre = db.Column(db.String(200), nullable=False)
	movies = db.relationship('Movie',secondary='genre_movies',back_populates='genre', lazy = 'select')


class Director(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	movies_dir = db.relationship('Movie', back_populates='director', lazy = 'select' )
	#PrimaryKeyConstraint('id')

#db.drop_all()

#db.create_all()

class Admin(Resource):
	#Add Admin
	#print("I am in IMDB_ADMIN class")
	@app.route('/IMDB/admin', methods = ['POST'])
	def new_admin(*args, **kwargs):
		print(args)
		print(kwargs)
		print("I am in new_user method")
		username = request.json.get('username')
		password = request.json.get('password')
		print(username)
		print(password)
		if username is None or password is None:
			abort(400) # missing arguments
		if Admin.query.filter_by(username = username).first() is not None:
			abort(400) # existing user
		admin = Admin(username = username)
		admin.hash_password(password)
		db.session.add(admin)
		db.session.commit()
		return jsonify({ 'username': admin.username }), 201

	#Authentication of admin
	@app.route('/IMDB/admin/login')
	@auth.login_required
	def get_resource():
		print("I am in get_resource")
		return jsonify({ 'data': 'Hello, %s!' % g.admin.username }), 201

	@auth.verify_password
	def verify_password(username, password):
		print("I am in verify password")
		print(username)
		print(password)
		admin = Admin.query.filter_by(username = username).first()
		print(admin)
		if not admin or not admin.verify_password(password):
			return False
		g.admin = admin
		return True


class User_resource(Resource):

		#Add user
	@app.route('/IMDB/user', methods = ['POST'])
	def new_user(*args, **kwargs):
		print(args)
		print(kwargs)
		print("I am in new_user method")
		username = request.json.get('username')
		password = request.json.get('password')
		print(username)
		print(password)
		if username is None or password is None:
			abort(400) # missing arguments
		if User.query.filter_by(username = username).first() is not None:
			abort(400) # existing user
		user = User(username = username)
		user.hash_password(password)
		db.session.add(user)
		db.session.commit()
		return jsonify({ 'username': user.username }), 201

	#Authentication of user
	@app.route('/IMDB/user/login')
	@auth.login_required
	def get_resource_user():
		return jsonify({ 'data': 'Hello, %s!' % g.user.username }), 201

	@auth.verify_password
	def verify_password_user(username, password):
		user = User.query.filter_by(username = username).first()
		if not user or not user.verify_password(password):
			return False
		g.user = user
		return True

class IMDB(Resource):
    
    #Add Movie
	@app.route('/IMDB/admin/add/movie', methods = ['POST'])
	def add_movie(*args, **kwargs):
		popularity = request.json.get('99popularity')
		director_name = request.json.get('director')
		genre = request.json.get('genre')
		imdb_score = request.json.get('imdb_score')
		name = request.json.get('name')
		print(popularity , director_name , genre , imdb_score, name  )
		if name is None :
			abort(400) # missing arguments
		if Movie.query.filter_by(name = name).first() is not None:
			abort(400) # existing movie
		if Director.query.filter_by(name = director_name).first() is not None:
			#existing director
			d = Director.query.filter_by(name = director_name).first()
			m = Movie(popularity = popularity, director_id=d.id, imdb_score = imdb_score,  name = name )
		else:
			d = Director(name = director_name)
			db.session.add(d)
			d = Director.query.filter_by(name = director_name).first()
			m = Movie(popularity = popularity, director_id=d.id, imdb_score = imdb_score,  name = name )
			d.movies_dir.append(m)
		
		for gen in genre:
				if Genre.query.filter_by(genre = gen).first() is not None:
					ge = Genre.query.filter_by(genre = gen).first()
					ge.movies.append(m)
					db.session.add(m)
				else:
					ge = Genre(genre = gen)
					db.session.add(ge)
					ge = Genre.query.filter_by(genre = gen).first()
					ge.movies.append(m)
					db.session.add(m)
	
		db.session.commit()
		return jsonify({ 'data' : 'Hello, Movie is successfully added.'}), 201


	@app.route('/IMDB/user/all', methods = ['GET'])
	def get_all_movies():

		movie = Movie.query.all()

		list1 = []

		for i in range(0,len(movie)):
			list1.append(movie[i].asdict())

		return jsonify(list1), 201

	@app.route('/IMDB/user/movie_by_name', methods = ['GET'])
	def get_movies_by_name():
		name = request.args.get('name')
		search = "{}%".format(name)
		m = Movie.query.filter(Movie.name.like(search)).all()
		list1 = []
		for i in range(0,len(m)):
			list1.append(m[i].asdict())

		return jsonify(list1), 201

	@app.route('/IMDB/user/score', methods = ['GET'])
	def get_movies_by_score():
		score = request.args.get('score')
		m = Movie.query.filter(Movie.imdb_score >= score).all()
		list1 = []
		for i in range(0,len(m)):
			list1.append(m[i].asdict())

		return jsonify(list1), 201


	@app.route('/IMDB/user/genre', methods = ['GET'])
	def get_movies_by_gnere():
		print("I am in get_movies_by_gnere")
		genre = request.args.get('genre')
		print(genre)
		ge = Genre.query.filter_by(genre = genre ).first()
		print(ge)
		m = Movie.query.filter(Movie.genre.contains(ge)).order_by(Movie.id).all()
		print(m)
		list1 = []
		for i in range(0,len(m)):
			list1.append(m[i].asdict())

		return jsonify(list1), 201

	@app.route('/IMDB/admin/delete', methods = ["GET"])
	def delete_movie(*args, **kwargs):
		name = request.args.get('name')
		print(name)
		m = Movie.query.filter_by(name = name ).first()
		print(m)
		db.session.delete(m)
		db.session.commit()
		return jsonify({"data":"Movie Deleted"}), 201

	@app.route('/IMDB/admin/update/movie', methods = ['POST'])
	def update_movie():
		id = request.json.get('id')
		m = Movie.query.filter_by(id = id).first()
		print(id)
		if 'popularity' in request.json:
			m.popularity = request.json.get('99popularity')
		if 'director' in request.json:
			director_name = request.json.get('director')
			if Director.query.filter_by(name = director_name).first() is not None:
			#existing director
				d = Director.query.filter_by(name = director_name).first()
				m.director_id = d.id
			else:
				d = Director(name = director_name)
				db.session.add(d)
				d = Director.query.filter_by(name = director_name).first()
				m.director_id = d.id
		if 'genre' in request.json:
			genre = request.json.get('genre')
			list1 = []
			for gen in genre:
				if Genre.query.filter_by(genre = gen).first() is not None:
					ge = Genre.query.filter_by(genre = gen).first()
					list1.append(ge)
				else:
					ge = Genre(genre = gen)
					db.session.add(ge)
					ge = Genre.query.filter_by(genre = gen).first()
					list1.append(ge)
			m.genre = list1
		if 'imdb_score' in request.json:
			m.imdb_score = request.json.get('imdb_score')
		if 'name' in request.json:
			m.name = request.json.get('name')

		db.session.commit()
		return jsonify({ 'data' : 'Hello, Movie is successfully updated'}), 201


api.add_resource(IMDB, "/IMDB/admin/login")


if __name__ == "__main__":
	app.run(debug=True, use_reloader=False)	