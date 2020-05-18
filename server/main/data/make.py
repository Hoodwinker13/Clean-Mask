import os

from elasticsearch import Elasticsearch
import pandas as pd
from datetime import datetime

class MakeDB() :
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")
        self.release_date = '20200509'

    def make_index(self, index_name="mask", doc_type="mask_data"):
        '''
        Make index(Database), if exists delete it
        '''
        params = {
            'index' : index_name,
            'body' : {
                'settings' : {
                    'number_of_shards' : 5,
                    'analysis' : {
                        'filter' : {
                            'ngram_filter' : {
                                'type' : 'edge_ngram',
                                'min_gram' : 1,
                                'max_gram' : 20,
                            },
                        },
                        'analyzer' : {
                            'ngram_analyzer' : {
                                'type' : 'custom',
                                'tokenizer' : 'standard',
                                'filter' : [
                                    'ngram_filter',
                                ],
                            }
                        }
                    }
                },
                'mappings' : {
                    'mask_data' : {
                        'properties' : {
                            'loading_particles' : {'type':'keyword'},
                            'mask_type' : {'type':'keyword'},
                            'name' : {'type':'keyword'},
                            'efficiency_0.3' : {'type':'keyword'},
                            'efficiency_0.5' : {'type':'keyword'},
                            'efficiency_1' : {'type':'keyword'},
                            'efficiency_3' : {'type':'keyword'},
                            'efficiency_5' : {'type':'keyword'},
                            'efficiency_10' : {'type':'keyword'},
                            'error_0.3' : {'type':'keyword'},
                            'error_0.5' : {'type':'keyword'},
                            'error_1' : {'type':'keyword'},
                            'error_3' : {'type':'keyword'},
                            'error_5' : {'type':'keyword'},
                            'error_10' : {'type':'keyword'},
                            'pa' : {'type':'keyword'},
                            'vair' : {'type':'keyword'},
                            't' : {'type':'keyword'},
                            'rh' : {'type':'keyword'},
                            'test_date' : {'type':'date'},
                        }
                    }
                },
            },
        }

        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
        print(self.es.indices.create(**params))

    def make_list_from_csv(self, index_name="mask", doc_type="mask_data"):
        csv_data = pd.read_csv('{}-Summary of New Masks.csv'.format(self.release_date),
                                header=1,
                                names=['loading_particles', 'mask_type', 'name', 'efficiency_0.3', 'efficiency_0.5',
                                        'efficiency_1', 'efficiency_3', 'efficiency_5', 'efficiency_10',
                                        'error_0.3', 'error_0.5', 'error_1', 'error_3', 'error_5', 'error_10',
                                        'pa', 'vair', 't', 'rh', 'test_date'
                                    ]
                            )
        for idx, data in csv_data.iterrows():
            doc = {
                'loading_particles' : data['loading_particles'],
                'mask_type' : data['mask_type'],
                'name' : data['name'],
                'efficiency_0.3' : data['efficiency_0.3'] if data['efficiency_0.3'] != '#DIV/0!' else 'null',
                'efficiency_0.5' : data['efficiency_0.5'] if data['efficiency_0.5'] != '#DIV/0!' else 'null',
                'efficiency_1' : data['efficiency_1'] if data['efficiency_1'] != '#DIV/0!' else 'null',
                'efficiency_3' : data['efficiency_3'] if data['efficiency_3'] != '#DIV/0!' else 'null',
                'efficiency_5' : data['efficiency_5'] if data['efficiency_5'] != '#DIV/0!' else 'null',
                'efficiency_10' : data['efficiency_10'] if data['efficiency_10'] != '#DIV/0!' else 'null',
                'error_0.3' : data['error_0.3'] if data['error_0.3'] != '#DIV/0!' else 'null',
                'error_0.5' : data['error_0.5'] if data['error_0.5'] != '#DIV/0!' else 'null',
                'error_1' : data['error_1'] if data['error_1'] != '#DIV/0!' else 'null',
                'error_3' : data['error_3'] if data['error_3'] != '#DIV/0!' else 'null',
                'error_5' : data['error_5'] if data['error_5'] != '#DIV/0!' else 'null',
                'error_10' : data['error_10'] if data['error_10'] != '#DIV/0!' else 'null',
                'pa' : data['pa'],
                'vair' : data['vair'],
                't' : data['t'],
                'rh' : data['rh'],
                'test_date' : datetime.strptime(data['test_date'], '%Y.%m.%d'),
            }
            res = self.es.index(index=index_name, doc_type=doc_type, id=idx+1, body=doc) # index에 insert
            print(res)
    
if __name__ == "__main__":
    db = MakeDB()
    db.make_index()
    db.make_list_from_csv()