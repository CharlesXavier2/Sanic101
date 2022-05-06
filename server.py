from sanic import Sanic, response
import redis
import json
import requests
from datetime import timedelta
##### INITIAL SETUP #####

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

redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
##### CRUD METHODS #####

@app.get('/')
async def get_student(request) :
    id = request.args.get("id")
    if id :
        return response.json(in_memory_student_db[int(id)])
    return response.json(in_memory_student_db)



@app.post('/')
async def post_student(request) :
    student = request.json
    in_memory_student_db.append(student)
    return response.json(student)

@app.put('/<id:int>')
async def update_student(request, id) :
    student = request.json
    if id in range(len(in_memory_student_db)):
        in_memory_student_db[id] = student
    else:
        return response.json({"error":"No Student with given id"})
    return response.json(student)

@app.delete('/<id:int>')
async def delete_student(request, id) :
    if id in range(len(in_memory_student_db)):
        del in_memory_student_db[id]
    else:
        return response.json({"error": "No Student with given id"})
    return response.json({"message": "Deleted student successfully"})

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

app.run(host='localhost', port=8000, debug=True,)