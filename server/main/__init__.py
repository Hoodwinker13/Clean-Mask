import json
import os

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


@main_bp.route('/search', methods=['GET'])
def search():
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

@main_bp.route('/completion', methods=['GET'])
def suggestion():
    name = request.args.get('name')

    '''
    query = {
        'prefix' : {
            'name' : name,
        }
    }
    '''
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

    return create_response(res, 200)

@main_bp.route('/fileUpload', methods=['POST'])
def fileUpload():
    file = request.files['file']

    try:
        file.save(os.path.join(file_path, secure_filename(file.filename)))
    except Exception:
        return 'Upload Error :('
    else:
        return 'Uploaded'