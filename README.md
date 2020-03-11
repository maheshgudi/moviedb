# Django Movie DB API

# Installation On Kubernetes

1. Install docker and kubectl.

2. Install minikube <https://kubernetes.io/docs/tasks/tools/install-minikube/>. This requires you to also install 
   a hypervisor. I went ahead with kvm-qemu. This requires Intel Virtualisation to be enabled from BIOS.

3. Start minikube with `minikube start`

4. Run `kubectl apply -f k8s-configs`
 

# Installation

1. Git clone the repo `https://github.com/maheshgudi/moviedb` or via ssh through `git@github.com:maheshgudi/moviedb.git`

2. Set-up and activate a **python3** virtualenv. preferably python3.7.6 or higher. Run `pip install -r requirements.txt` to install
   dependencies.

3. Run the server by running the command ```python manage.py runserver```. Run migrations beforehand.

4. Run the following command to upload sample files.

```
python manage.py upload_movies movie_file movies/imdb.json
```

5. Create superuser using the command `python manage.py createsuperuser`.

6. Login into the admin panel and create a group `Administrator` with all permissions for `Movie` Model. 

7. Admin can add registered users into the `Administrator` group. The user can then be able to create, delete, and update movie from API endpoints.

8. Admin password is `username-admin, password-admin` to access the heroku server for the same.

9. Heroku API server can be found on the following <https://django-moviedb.herokuapp.com/>


# REST API Documentation 

This server acts as a REST API server to search, add, edit and delete database of movies.

# Routes

### `/` and `/api/`

##### Returns
Returns the `OpenAPI Schema` for the API. This is useful to discover and understand the capabilities of the service.


### `/admin/`

##### Returns
Login into the Django admin panel. All models are registered in the admin page.

### `POST api/register/`

##### Expects

Add following JSON Fields in the POST Body.

```
{
    "username": "<username>",
    "email": "<email>",
    "password": "<password>",
    "first_name": "<first_name>",
    "last_name": "<last_name>"
}
```

##### Returns
If `Username` and/or `email` is not registered previously, User is created and token is returned, as shown below,

```
{'token': <token_id>,
 'status': True,
 'message': 'User created successfully'}
```

**Note: Please save the token and use it in the headers for all future API calls.**


### `GET /api/allmovies/`
**Note: User needs to be registered to be able to access this feature.**

##### Expects

Add in JSON request Header

```
{'Authorization': 'token <token_id>'}
```

##### Returns
Returns all movies stored in the db as in `JSON` format. 


### `GET /api/movies/<movie_id>`
**Note: User needs to be an admin and have a admin token to be able to access this feature.**

##### Expects

Add in JSON request Header

```
{'Authorization': 'token <token_id>'}
```

##### Returns 

Returns the Movie details.

```
{
    "status":true,
    "movie_id":"74826d60-6c42-4221-86a9-d283ed6f6946",
    "name":"The Wizard of Oz",
    "director":"Victor Fleming",
    "imdb_score":8.3,
    "popularity":83.0,
    "genres":["Adventure","Family","Fantasy","Musical"]
}
```

### `DELETE /api/movies/<movie_id>`

##### Expects

Add in JSON request Header

```
{'Authorization': 'token <token_id>'}
```

##### Returns 

Returns the deleted movie details.

```
{
    "status":true,
    "message":"<movie_name> deleted successfully"
}
```


### `PUT /api/movies/<movie_id>`

##### Expects

Add in JSON request Header

```
{'Authorization': 'token <token_id>'}
```

and add in PUT body

```
{
    "movie_id":"74826d60-6c42-4221-86a9-d283ed6f6946",
    "name":"The Wizard of Oz",
    "director":"Victor Fleming, Mahesh Gudi",
    "imdb_score":8.3,
    "popularity":83.0,
    "genres":["Adventure","Family","Fantasy","Musical"]
}
NOTE: Director name is being updated with this POST Body. One can ignore movie_id while posting.
If however, one does add a movie id, it will still not update the original movie id.
```


##### Returns 

Returns the Movie details.

```
{
    "status":true,
    "movie_id":"74826d60-6c42-4221-86a9-d283ed6f6946",
    "name":"The Wizard of Oz",
    "director":"Victor Fleming, Mahesh Gudi",
    "imdb_score":8.3,
    "popularity":83.0,
    "genres":["Adventure","Family","Fantasy","Musical"]
}
```


### `POST /api/movies/`

##### Expects

Add in JSON request Header

```
{'Authorization': 'token <token_id>'}
```

and add in POST body

```
[
  {
    "99popularity": 83.0,
    "director": "Mahesh Gudi",
    "genre": [
      "Adventure",
      " Family",
      " Fantasy",
      " Musical"
    ],
    "imdb_score": 8.3,
    "name": "The Wizard of Oz"
  },
  {
    "99popularity": 88.0,
    "director": "Mahesh Gudi",
    "genre": [
      "Action",
      " Adventure",
      " Fantasy",
      " Sci-Fi"
    ],
    "imdb_score": 8.8,
    "name": "Star Wars"
  }
]
```


##### Returns 

Returns the Movie details.

```
{'status': True,
 'data': [{'movie_id': 'da00e02a-7b8b-4aeb-af48-60e35c2d7d41',
   'name': 'The Wizard of Oz',
   'director': 'Mahesh Gudi',
   'imdb_score': 8.3,
   'popularity': 83.0,
   'genres': ['Adventure', 'Family', 'Fantasy', 'Musical']},
  {'movie_id': '235835bb-33fa-48d5-aafc-4412930ecbda',
   'name': 'Star Wars',
   'director': 'Mahesh Gudi',
   'imdb_score': 8.8,
   'popularity': 88.0,
   'genres': ['Adventure', 'Fantasy', 'Action', 'Sci-Fi']}]}

```


### `GET /api/search/?<name|director|imdb_score|popularity|genre>`
**Note: Any user can search for movies. No authentication token required.**

##### Expects

Search for the following get parameters i.e. `name, director, imdb_score, popularity, genre`. One can search with only one params or even many.
Each param can have only one value.
For e.g. -

```
GET /api/search/?director=martin
```

will return 

```
{
    "status": true,
    "data": [
        {
            "movie_id": "f11ec718-ee06-4175-9bc4-be093e37ec18",
            "name": "Taxi Driver",
            "director": "Martin Scorsese",
            "imdb_score": 8.6,
            "popularity": 86.0,
            "genres": [
                "Drama",
                "Thriller"
            ]
        },
        {
            "movie_id": "b3c3ac74-915c-4107-8273-25f1494b2d78",
            "name": "Goodfellas",
            "director": "Martin Scorsese",
            "imdb_score": 8.8,
            "popularity": 88.0,
            "genres": [
                "Drama",
                "Thriller",
                "Crime"
            ]
        }
    ]
}
```

While adding more query params 


```
GET /api/search/?director=martin?name=good
```

will return 

```
{
    "status": true,
    "data": [
        {
            "movie_id": "b3c3ac74-915c-4107-8273-25f1494b2d78",
            "name": "Goodfellas",
            "director": "Martin Scorsese",
            "imdb_score": 8.8,
            "popularity": 88.0,
            "genres": [
                "Drama",
                "Thriller",
                "Crime"
            ]
        }
    ]
}
```
