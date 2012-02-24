import json
import query
import httplib

class ElasticSearchModel:

    def __init__(self, obj):
        self.__obj = obj

    @property
    def object_json_format(self):
        return self.__obj

class DataCollection:

    def __init__(self, data):
        self.__data_obj = json.loads(data)
        self.__collection = []
        self.__ind = 0
        self.__build_collection()

    def __json_to_model(self, json_obj):
        ret = None

        if isinstance(json_obj, dict):
            ret = ElasticSearchModel(json_obj)

            for item in json_obj:
                value = None
                if isinstance(json_obj[item], dict) or isinstance(json_obj[item], list):
                    value = self.__json_to_model(json_obj[item])
                else:
                    value = json_obj[item]

                setattr(ret, item, value)

        elif isinstance(json_obj, list):
            ret = []

            for item in json_obj:
                if isinstance(item, dict) or isinstance(item, list):
                    ret.append(self.__json_to_model(item))
                else:
                    ret.append(item)

        return ret

    def __build_collection(self):

        if self.total > 0:
            for item in self.__data_obj['hits']['hits']:
                self.__collection.append(self.__json_to_model(item['_source']))

    @property
    def total(self):
        return self.__data_obj['hits']['total']

    def next(self):
        if self.__ind == self.total:
            self.__ind = 0
            raise StopIteration

        self.__ind += 1
        return self.__collection[self.__ind - 1]

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self.__collection[key]

    def __len__(self):
        return self.total


class ElasticSearch:

    def __init__(self, host, port):
        self.__connection = httplib.HTTPConnection(host, port)

    def __request (self, url, method, body_request = None):
        self.__connection.request(method, url, body = body_request)
        response = self.__connection.getresponse()
        return (response.status, response.read())

    def index(self, document, index, document_type, document_id = None):
        url = '/%s/%s' % (index, document_type)
        method = None

        if document_id != None:
            method = 'PUT'
            url = '%s/%s' % (url, document_id)
        else:
            method = 'POST'

        resp, content = self.__request(url, method, document)
        return resp

    def refresh(self, index):
        url = None

        if isinstance(index, list):
            t = len(inde)
            url = ''
            if t > 0:
                url += index[0]

                for i in range(1, t):
                    url += ',%s' % index[i]
        else:
            url = '/%s/_refresh' % index

        self.__request(url, 'POST')

    def query(self, query, index, document_type):
        query.build_query()
        resp, content = self.__request('/%s/%s/_search/' % (index, document_type), 'GET', query.get_query())
        return DataCollection(content)

    def count(self, query, index, document_type):
        query.build_query()
        resp, content = self.__request('/%s/%s/_count/' % (index, document_type), 'GET', query.get_object_json())
        t = json.loads(content)
        return t[u'count']
