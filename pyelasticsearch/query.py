import json

class Query(object):

    def __init__(self):
        self._query_object = None

    def build_query(self): pass

    def get_query(self):
        return json.dumps({ 'query' : self._query_object})

    def get_object(self):
        return self._query_object

class TermQuery(Query):

    def __init__(self, term, value):
        self.__term = term
        self.__value = value

    def build_query(self):
        self._query_object = {'term' : {self.__term : self.__value}}

class TermsQuery(Query):

    def __init__(self, term, list_value):
        self.__term = term
        self.__list_value = list_value

    def build_query(self):
        self._query_object = {'terms' : {self.__term : self.__list_value}}