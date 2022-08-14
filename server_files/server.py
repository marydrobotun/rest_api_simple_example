#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import json
import yaml

app = Flask(__name__)
import pymongo
import os

config = yaml.full_load(open('config.yaml'))
conn = pymongo.MongoClient(username=os.environ['mongo_login'], password=os.environ['mongo_password'],
                           host=config['db']['host'], port=config['db']['port'])


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    result = []
    for task in conn.tasks['tasks'].find():
        del task['_id']
        result.append(task)
    return jsonify(result)


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [x for x in conn.tasks['tasks'].find() if x['id'] == task_id]
    if len(task) == 0:
        abort(404)
    del task[0]['_id']
    return jsonify({'task': task[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    tasks = (x for x in conn.tasks['tasks'].find())
    id = 1
    for task in tasks:
        if task['id'] > id:
            id = task['id']

    task = {
        'id': id + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }

    conn.tasks['tasks'].insert(task)
    del task['_id']
    return jsonify({'task': task}), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [x for x in conn.tasks['tasks'].find() if x['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    mongo_id = {'_id': task[0]['_id']}
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    del task[0]['_id']
    conn.tasks['tasks'].update(mongo_id, task[0])
    return jsonify({'task': task[0]})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [x for x in conn.tasks['tasks'].find() if x['id'] == task_id]
    if len(task) == 0:
        abort(404)
    mongo_id = task[0]['_id']
    conn.tasks['tasks'].remove({'_id': mongo_id})
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(host='web', port=80, debug=True, use_reloader=False)
