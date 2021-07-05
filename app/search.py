from flask import current_app
from .helpers import conf


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        # This if is for JSON field in the db (they have to be parsed to string
        if type(getattr(model, field)) is dict:
            payload[field] = str(getattr(model, field))
        else:
            payload[field] = getattr(model, field)

    if conf('indices_postfix'):
        index += conf('indices_postfix')

    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return

    if conf('indices_postfix'):
        index += conf('indices_postfix')

    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query):
    if not current_app.elasticsearch:
        return [], 0

    if conf('indices_postfix'):
        index += conf('indices_postfix')

    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}}})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
