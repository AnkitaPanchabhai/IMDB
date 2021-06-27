import requests
import json

BASE = "http://127.0.0.1:5000/"

#Test case to create admin
#response = requests.post(BASE+"IDBM/admin" ,json={'username': 'Ross', 'password': 'Ross'})

#Admin authentication
#response = requests.get(BASE + "IDBM/admin/login" , json={'username': 'ankita', 'password': 'admin'} )

#Add user
#response = requests.post(BASE+"IMDB/user" ,json={'username': 'John', 'password': 'john45?8'})
#response = requests.post(BASE+"IDBM/user" ,json={'username': 'Rina', 'password': 'Ri#45'})
#response = requests.post(BASE+"IDBM/user" ,json={'username': 'Alexa', 'password': 'Al&78nb'})
#response = requests.post(BASE+"IDBM/user" ,json={'username': 'Lily', 'password': 'Lily90'})
#response = requests.post(BASE+"IDBM/user" ,json={'username': 'Jamal', 'password': 'IamJamal@5'})

#Get user
#response = requests.get(BASE + "IMDB/user/login" , json={'username': 'John', 'password': 'joh45?8n'} )

#add movie
#response = requests.post(BASE+"IMDB/admin/add/movie" ,
#json= {
 #   "99popularity": 87.0,
 #   "director": "Alfred Hitchcock",
 #   "genre": [
 #     "Crime",
  #    "Mystery",
   #   "Romance",
    #  "Thriller"
    #],
    #"imdb_score": 8.7,
    #"name": "Rear Window"
  #})

#
#response = requests.post(BASE+"IDBM/admin/add/movie" ,
#json=
#{
#    "99popularity": 68.0,
#    "director": "George Lucas",
#    "genre": [
#      "Drama",
#      " Horror",
#      " Sci-Fi",
#      " Adeventure"
#    ],
#    "imdb_score": 6.8,
#    "name": "AAA"
#   })



#response = requests.post(BASE+"IMDB/admin/add/movie" ,
#json=
#{
#   "99popularity": 68.0,
 # "director": "George Lucas",
 # "genre": [
 #   "Drama",
 #    " Mystery",
 #    " Sci-Fi",
 #    " Thriller"
 #   ],
 #  "imdb_score": 6.8,
 #   "name": "VAX"
 #})

#get all movies
#response = requests.get(BASE + "IMDB/user/all")

#response = requests.get(BASE + "IMDB/user/movie_by_name", json={"name" : 'Vertigo'})
#response = requests.get(BASE + "IMDB/admin/delete")

#update the movie
#response = requests.post(BASE + "IMDB/admin/update/movie",json={"id" : 3, "name" : "Yolo", "director": "BTS", "genre": ["DD", "Adventure"]})


