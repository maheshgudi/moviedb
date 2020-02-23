# Django Movie DB API

@Note to self: add django custom management commands and stuff on how to deploy on heroku

# REST API Documentation 

This server acts as a REST API server to search, add, edit and delete database of movies.

# Routes

### `/` and `/api/`

##### Returns
Returns the `OpenAPI Schema` for the API. This is useful to discover and understand the capabilities of the service.


### `/admin/`

##### Returns
Used to login into the Django admin panel. All models are registered in the admin page.

### `api/register/`

##### Expects

Following JSON Fields

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

**Note: Please save the token and use it for all future API calls.**


### `/api/allmovies/`

##### Expects

Add in JSON request Header

```
{'Authorization': 'token <token_id>'}
```

##### Returns
Returns all movies stored in the db as in `JSON` format. 


### `/api/movies/<movie_id>`
**Note: User needs to be an admin and have a admin token to be able to access this feature.**

#### GET Method

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

#### DELETE Method

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
    "message":"<movie_name> deleted successfully"
}
```


#### PUT Method

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


### `/api/movies/`
**Note: User needs to be an admin and have a admin token to be able to access this feature.**

#### POST Method

##### Expects

Add in JSON request Header

```
{'Authorization': 'token <token_id>'}
```

and add in POST body

```

```


##### Returns 

Returns the Movie details.


### `/api/search/?<name|director|imdb_score|popularity|genre>`
**Note: Any user can search for movies. No authentication token required.**

#### GET Method

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
