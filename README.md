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

and add in PUT body add 

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


##### Returns 

Returns the Movie details.

```
{
    "status":true,
    "message":"<movie_name> deleted successfully"
}
```
