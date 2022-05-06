from sanic import Sanic, response

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

##### RUN SERVER #####

app.run(host='localhost', port=8000, debug=True,)