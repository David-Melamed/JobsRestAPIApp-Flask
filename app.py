import json
from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

jobs = [
  {
    'id': 1,
    'title': 'DevOps Engineer',
    'description': 'description7',
    'timestamp': datetime.datetime.now()
    }
]

nextjobId = 2

@app.route('/jobs', methods=['GET'])
def get_jobs():
  return jsonify(jobs)


def job_is_valid(job):
  for key in job.keys():
    print(key)
    if key != 'title' and key != 'description':
      return False
  return True

@app.route('/jobs', methods=['POST'])
def create_job():
  global nextjobId
  job = json.loads(request.data)
  if not job_is_valid(job):
    return jsonify({ 'error': 'Invalid job properties.' }), 400

  job['id'] = nextjobId
  job['timestamp'] = datetime.datetime.now()
  nextjobId += 1
  jobs.append(job)

  return '', 201, { 'location': f'/jobs/{job["id"]}' }


def get_job(id):
  return next((e for e in jobs if e['id'] == id), None)

@app.route('/jobs/<int:id>', methods=['DELETE'])
def delete_job(id: int):
  global jobs
  job = get_job(id)
  if job is None:
    return jsonify({ 'error': 'job does not exist.' }), 404

  jobs = [e for e in jobs if e['id'] != id]
  return jsonify(job), 200

app.run(debug=True,host='0.0.0.0',port=5000)