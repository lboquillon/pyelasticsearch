=============================
pyelasticsearch - Minimalist python elasticsearch query library
=============================


Usage mode:
=============================

>>> obj = {'name' : 'leonardo', 'age' : 20, 'food' : ['rice', 'soda', 'cheese']}
NameError: name 'ElasticSearch' is not defined
>>> cnn = core.ElasticSearch('127.0.0.1', 9200)
>>> cnn.index(obj, 'test', 'people')
201
>>> termquery = query.TermQuery('name', 'leonardo')
>>> datacll = cnn.query(termquery, 'test', 'people')
>>> for people in datacll:
...     print people.name
...
leonardo
>>> for people in datacll:
...     for food in people.food:
...             print food
...
rice
soda
cheese
>>> datacll[0].object_json_format
{u'food': [u'rice', u'soda', u'cheese'], u'age': 20, u'name': u'leonardo'}