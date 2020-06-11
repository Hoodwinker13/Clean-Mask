import os

from elasticsearch import Elasticsearch
import pandas as pd
from datetime import datetime

class MakeDB() :
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")
        self.release_date = '20200509'

    def make_index_data(self, index_name="mask_data"):
        '''
        Make index(Database), if exists delete it
        '''
        params = {
            'index' : index_name,
            'body' : {
                'settings' : {
                    'number_of_shards' : 5,
                },
                'mappings' : {
                    'mask_data' : {
                        'properties' : {
                            'loading_particles' : {'type':'keyword'},
                            'mask_type' : {'type':'keyword'},
                            'name' : {'type':'keyword'},
                            'efficiency_03' : {'type':'keyword'},
                            'efficiency_05' : {'type':'keyword'},
                            'efficiency_1' : {'type':'keyword'},
                            'efficiency_3' : {'type':'keyword'},
                            'efficiency_5' : {'type':'keyword'},
                            'efficiency_10' : {'type':'keyword'},
                            'error_03' : {'type':'keyword'},
                            'error_05' : {'type':'keyword'},
                            'error_1' : {'type':'keyword'},
                            'error_3' : {'type':'keyword'},
                            'error_5' : {'type':'keyword'},
                            'error_10' : {'type':'keyword'},
                            'pa' : {'type':'keyword'},
                            'vair' : {'type':'keyword'},
                            't' : {'type':'keyword'},
                            'rh' : {'type':'keyword'},
                            'test_date' : {'type':'date'},
                            'test_city' : {'type':'keyword'},
                            'comment' : {'type': 'text'},
                            'username' : {'type': 'keyword'},
                            'img_name' : {'type':'text'},
                        }
                    },
                },
            },
        }

        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
        print(self.es.indices.create(**params))
    
    def make_index_completion(self, index_name="mask_completion"):
        '''
        Make index(Database), if exists delete it
        '''
        params = {
            'index' : index_name,
            'body' : {
                'settings' : {
                    'number_of_shards' : 5,
                },
                'mappings' : {
                    'mask_completion' : {
                        'properties' : {
                            'name' : {'type':'completion'},
                        }
                    },
                },
            },
        }

        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
        print(self.es.indices.create(**params))

    def make_list_from_csv(self, index_name="mask_data", doc_type="mask_data", index_name2="mask_completion", doc_type2="mask_completion"):
        csv_data = pd.read_csv('{}-Summary of New Masks.csv'.format(self.release_date),
                                header=1,
                                names=['loading_particles', 'mask_type', 'name', 'efficiency_03', 'efficiency_05',
                                        'efficiency_1', 'efficiency_3', 'efficiency_5', 'efficiency_10',
                                        'error_03', 'error_05', 'error_1', 'error_3', 'error_5', 'error_10',
                                        'pa', 'vair', 't', 'rh', 'test_date'
                                    ]
                            )
        for idx, data in csv_data.iterrows():
            doc_data = {
                'loading_particles' : data['loading_particles'],
                'mask_type' : data['mask_type'],
                'name' : data['name'],
                'efficiency_03' : data['efficiency_03'] if data['efficiency_03'] != '#DIV/0!' else 'null',
                'efficiency_05' : data['efficiency_05'] if data['efficiency_05'] != '#DIV/0!' else 'null',
                'efficiency_1' : data['efficiency_1'] if data['efficiency_1'] != '#DIV/0!' else 'null',
                'efficiency_3' : data['efficiency_3'] if data['efficiency_3'] != '#DIV/0!' else 'null',
                'efficiency_5' : data['efficiency_5'] if data['efficiency_5'] != '#DIV/0!' else 'null',
                'efficiency_10' : data['efficiency_10'] if data['efficiency_10'] != '#DIV/0!' else 'null',
                'error_03' : data['error_03'] if data['error_03'] != '#DIV/0!' else 'null',
                'error_05' : data['error_05'] if data['error_05'] != '#DIV/0!' else 'null',
                'error_1' : data['error_1'] if data['error_1'] != '#DIV/0!' else 'null',
                'error_3' : data['error_3'] if data['error_3'] != '#DIV/0!' else 'null',
                'error_5' : data['error_5'] if data['error_5'] != '#DIV/0!' else 'null',
                'error_10' : data['error_10'] if data['error_10'] != '#DIV/0!' else 'null',
                'pa' : str(round(float(data['pa']),2)),
                'vair' : data['vair'],
                't' : data['t'],
                'rh' : data['rh'],
                'test_date' : datetime.strptime(data['test_date'], '%Y.%m.%d'),
                'test_city' : 'null',
                'comment' : 'null',
                'username' : 'null',
                'img_name' : 'null',
            }
            doc_name = {
                'name' : data['name'],
            }
            res_data = self.es.index(index=index_name, doc_type=doc_type, id=idx+1, body=doc_data) # index에 insert
            res_name = self.es.index(index=index_name2, doc_type=doc_type2, id=idx+1, body=doc_name)
            print(res_data, res_name)
    
if __name__ == "__main__":
    db = MakeDB()
    db.make_index_data()
    db.make_index_completion()
    db.make_list_from_csv()