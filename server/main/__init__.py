import json
import os
from datetime import datetime
import uuid

import werkzeug
from werkzeug.utils import secure_filename

werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect

from .config import config_by_name

from elasticsearch import Elasticsearch

main_bp = Blueprint("main", __name__)
cfg = config_by_name[os.getenv("FLASK_ENV", "dev")]
img_static = cfg.FILE_PATH

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
@main_bp.route('/index')
def index():
    return render_template('index.html')
@main_bp.route('/about')
def about():
    return render_template('about.html')
@main_bp.route('/setup')
def setup():
    return render_template('setup.html')
@main_bp.route('/procedures')
def procedures():
    return render_template('procedures.html')
@main_bp.route('/data')
def data():
    return render_template('data.html')
@main_bp.route('/data_input')
def data_input():
    return render_template('data_input.html')
@main_bp.route('/')
def random():
    return redirect('/index')
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
            'sort': {
                'name':'asc'
            },
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

@main_bp.route('/update', methods=['POST'])
def update() :
    data = json.loads(request.form['mask_data'])

    try:
        doc_data = {
                    'loading_particles' : data['loading_particles'],
                    'mask_type' : data['mask_type'],
                    'name' : data['name'],
                    'efficiency_03' : data['efficiency_03'],
                    'efficiency_05' : data['efficiency_05'],
                    'efficiency_1' : data['efficiency_1'],
                    'efficiency_3' : data['efficiency_3'],
                    'efficiency_5' : data['efficiency_5'],
                    'efficiency_10' : data['efficiency_10'],
                    'error_03' : data['error_03'],
                    'error_05' : data['error_05'],
                    'error_1' : data['error_1'],
                    'error_3' : data['error_3'],
                    'error_5' : data['error_5'],
                    'error_10' : data['error_10'],
                    'pa' : data['pa'],
                    'vair' : data['vair'],
                    't' : data['t'],
                    'rh' : data['rh'],
                    'test_date' : datetime.strptime(data['test_date'], '%Y.%m.%d'),
                    'test_city' : data['test_city'],
                    'comment' : data['comment'],
                    'username' : data['username'],
                }
        doc_name = {
                    'name' : data['name'],
                }
    except KeyError:
        return create_response('missing parameter', 400)
    except ValueError:
        return create_response('Data format Error', 400)

    try:
        file = request.files['file']
    except Exception as e:
        return create_response('File Upload Error', 400)

    res_data = es.index(index='mask_data', doc_type='mask_data', body=doc_data) # index에 insert
    res_name = es.index(index='mask_completion', doc_type='mask_completion', body=doc_name)
    file.save(os.path.join(img_static, str(uuid.uuid4())+os.path.splitext(file.filename)[1]))

    if not (isinstance(res_data, dict) or isinstance(res_name, dict)):
        return create_response('failed', 400)
    else:
        return create_response('success', 200)
    