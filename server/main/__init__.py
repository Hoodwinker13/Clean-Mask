import json
import os
from datetime import datetime

import werkzeug
from werkzeug.utils import secure_filename

werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Blueprint
from flask import Response
from flask import request

from .config import config_by_name

from elasticsearch import Elasticsearch

main_bp = Blueprint("main", __name__)
cfg = config_by_name[os.getenv("FLASK_ENV", "dev")]
file_path = cfg.FILE_PATH

es = Elasticsearch(cfg.ES_HOST)

def create_response(body, status, content_type="application/json;charset=utf-8", headers=None,
                    mimetype="application/json;charset=utf-8", direct_passthrough=False):
    params = {
        "response": json.dumps(body),
        "status": status,
        "content_type": content_type,
        "headers": headers,
        "mimetype": mimetype,
        "direct_passthrough": direct_passthrough,
    }
    return Response(**params)


@main_bp.route('/ping', methods=['GET'])
def get():
    '''
    Server Health Checker
    '''
    body = {
        'message': 'pong',
    }
    return create_response(body, 200)


@main_bp.route('/search', methods=['POST'])
def search():
    if request.headers['Content-Type'] == 'application/json' :
        data = request.get_json()
        name = data['name']
    else:
        name = request.args.get('name')

    query = {
        'match' : {
            'name' : {
                'query' : name,
                'fuzziness' : 2,
            }
        }
    }

    res = es.search(
        index='mask_data',
        doc_type='mask_data',
        body={
            'query' : query,
        },
    )

    return create_response(res, 200)

@main_bp.route('/getAll', methods=['POST'])
def allData():
    res = es.search(
        index='mask_data',
        doc_type='mask_data',
        body={
            'query':{
                'match_all' : {},
            },
            'size' : 100
        }
    )

    return create_response(res, 200)


@main_bp.route('/completion', methods=['POST'])
def suggestion():
    if request.headers['Content-Type'] == 'application/json' :
        data = request.get_json()
        name = data['name']
    else:
        name = request.args.get('name')

    query = {
        'completion' : {
            'prefix' : name,
            'completion' : {
                'field' : 'name',
                'size' : 5,
            }
        }
    }

    res = es.search(
        index='mask_completion',
        doc_type='mask_completion',
        body={
            'suggest':query,
        },
    )

    completion_list = []
    res_data = res['suggest']['completion'][0]['options']
    for completion in res_data:
        completion_list.append(completion['text'])

    return create_response({
        'names' : completion_list,
        'length' : len(completion_list)
    }, 200)

@main_bp.route('/fileUpload', methods=['POST'])
def fileUpload():
    file = request.files['file']

    try:
        file.save(os.path.join(file_path, secure_filename(file.filename)))
    except Exception:
        return 'Upload Error :('
    else:
        return 'Uploaded'

@main_bp.route('/update', methods=['POST'])
def update() :
    data = request.get_json()

    try:
        doc_data = {
                    'loading_particles' : data['loading_particles'],
                    'mask_type' : data['mask_type'],
                    'name' : data['name'],
                    'efficiency_0.3' : data['efficiency_0.3'],
                    'efficiency_0.5' : data['efficiency_0.5'],
                    'efficiency_1' : data['efficiency_1'],
                    'efficiency_3' : data['efficiency_3'],
                    'efficiency_5' : data['efficiency_5'],
                    'efficiency_10' : data['efficiency_10'],
                    'error_0.3' : data['error_0.3'],
                    'error_0.5' : data['error_0.5'],
                    'error_1' : data['error_1'],
                    'error_3' : data['error_3'],
                    'error_5' : data['error_5'],
                    'error_10' : data['error_10'],
                    'pa' : data['pa'],
                    'vair' : data['vair'],
                    't' : data['t'],
                    'rh' : data['rh'],
                    'test_date' : datetime.strptime(data['test_date'], '%Y.%m.%d'),
                }
        doc_name = {
                    'name' : data['name'],
                }
    except KeyError:
        return create_response('missing parameter', 400)
    except ValueError:
        return create_response('Data format Error', 400)

    res_data = es.index(index='mask_data', doc_type='mask_data', body=doc_data) # index에 insert
    res_name = es.index(index='mask_completion', doc_type='mask_completion', body=doc_name)

    if not (isinstance(res_data, dict) or isinstance(res_name, dict)):
        return 'Failed to Update :('
    else:
        return 'Success!'
    