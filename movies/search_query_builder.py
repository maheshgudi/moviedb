QUERY_CONFIG = {
    "name": lambda x: {"name__icontains": x},
    "director": lambda x: {"director__icontains": x},
    "imdb_score": lambda x: {"imdb_score":x },
    "popularity": lambda x: {"popularity": x},
    "genre": lambda x: {"genre__name__icontains": x}
    }

def build_query(params):
    filter_query = {}
    for k, v in params.items():
        query = QUERY_CONFIG.get(k)
        if query:
            filter_query.update(query(v))
    return filter_query