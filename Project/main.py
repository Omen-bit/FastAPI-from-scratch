from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()


def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}


@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}


@app.get('/view')
def view():
    data = load_data()
    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', examples='p001')):
    data = load_data()

    print("DEBUG: keys in data =", data.keys())
    print("DEBUG: requested patient_id =", patient_id)

    if patient_id in data:
        print("DEBUG: found record =", data[patient_id])
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not Found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid entered fields select from {valid_fields}')

    if order not in ['asc', 'dsc']:
        raise HTTPException(status_code=400, detail='Invalid entered order')

    data=load_data()

    sort_order = True if order=='dsc' else False

    sorted_values=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_values

