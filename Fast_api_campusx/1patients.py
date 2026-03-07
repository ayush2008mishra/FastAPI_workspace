from fastapi import FastAPI    #importing FastAPI class from fastapi
import json

#making object of class FastAPI
app = FastAPI()


def load_data():
    with open("1patients.json","r") as f:
        data = json.load(f)             #data as dictionary
    return data


#using decorators to make the end points - by me
@app.get("/")  #get request and  "/" is raute
def hello():
    return {"message":"Patients Management System API"}

@app.get("/About")
def about():
    return {"meassge":"A fully functional api to manage your pateints records fuck you"}

@app.get("/view")
def view():
    data = load_data()
    return data





# now in order to run type this in terminal
# uvicorn {fileName without .py}:{objectName} --reload