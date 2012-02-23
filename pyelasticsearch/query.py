import json

class Query(object):

    def __init__(self):
        self._query_object = None

    def build_query(self): pass

    def get_query(self):
        return json.dumps({ 'query' : self._query_object})

    def get_object(self):
        return self._query_object

class RangeQuery(Query):

    def __init__(self, field, from_, to_, include_lower = False, include_upper = False):
        super(RangeQuery, self).__init__()
        self.__field = field
        self.__from = from_
        self.__to = to_
        self.__in_lo = include_lower
        self.__in_up = include_upper

    def build_query(self):

        self._query_object = {'range' : {}}
        self._query_object['range'][self.__field] = {'from' : self.__from, 'to' : self.__to, 'include_lower' : self.__in_lo, 'include_upper' : self.__in_up}

class TermQuery(Query):

    def __init__(self, term, value):
        super(TermQuery, self).__init__()
        self.__term = term
        self.__value = value

    def build_query(self):
        self._query_object = {'term' : {self.__term : self.__value}}

class TermsQuery(Query):

    def __init__(self, term, list_value):
        super(TermsQuery, self).__init__()
        self.__term = term
        self.__list_value = list_value

    def build_query(self):
        self._query_object = {'terms' : {self.__term : self.__list_value}}