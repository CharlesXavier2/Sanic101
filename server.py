from sanic import Sanic, response
import redis
import json
from bson import ObjectId

import requests
from datetime import timedelta
from pymongo import MongoClient
from pprint import pprint


##### SANIC INITIAL SETUP #####

app = Sanic('school')

in_memory_student_db = [ 
    {
        'name' : 'Abhinav Mishra',
        'grade' : 12,
        'roll' : 1,
        'email' : 'ab@g.com',
        'contact' : '7830236194'
    }
]

##### REDIS INITIAL SETUP #####
redis_client = redis.Redis(host='localhost', port=6379, db=0)

##### MONGO INITIAL SETUP #####
db_client = MongoClient('mongodb://localhost:27017/')
db  = db_client.school
    
##### CRUD METHODS #####

@app.get('/')
async def get_student(request) :
    id = request.args.get("id")
    if id :
        student = db.student.find_one({"_id":ObjectId(id)})
        pprint(id)
        return response.json(student, default=str, dumps=json.dumps)
    students = db.student.find()
    res = []
    for student in students : 
        res.append(student)
    return response.json(res, default=str)


# @app.post('/')
# async def post_student(request) :
#     student = request.json
#     created_student = db.student.insert_one(student)
    
#     return response.json(created_student, default=str)

# @app.put('/<id:int>')
# async def update_student(request, id) :
#     student = request.json
#     if id in range(len(in_memory_student_db)):
#         in_memory_student_db[id] = student
#     else:
#         return response.json({"error":"No Student with given id"})
#     return response.json(student)

# @app.delete('/<id:int>')
# async def delete_student(request, id) :
#     if id in range(len(in_memory_student_db)):
#         del in_memory_student_db[id]
#     else:
#         return response.json({"error": "No Student with given id"})
#     return response.json({"message": "Deleted student successfully"})

##### REDIS CACHING OF AN API CALL #####
@app.get('/redis')
async def get_redis_cache(request) :
    

    api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response_json =  {}

    api_data = redis_client.get('api_data')
    redis_client.expire('api_data', timedelta(seconds=5))
    if api_data :
        print('Serving From Redis Cache') 
        response_json = json.loads(api_data)
        return response.json({'msg' : 'Serving From Redis Cache'})
    else :
        print('Serving From Web API') 
        res = requests.get(api_url)
        response_json = res.json()
        redis_client.set('api_data', json.dumps(res.json()))
        return response.json({'msg' : 'Serving From Web API'})
    

##### RUN SERVER #####

app.run(host='localhost', port=8000, debug=True, auto_reload=True)