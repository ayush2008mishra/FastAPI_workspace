#from CampusX


from fastapi import FastAPI    #importing FastAPI class from fastapi

#making object of class FastAPI
app = FastAPI()

#using decorators to make the end points - by me
@app.get("/")  #get request and  "/" is raute
def hello():
    return {"message":"hello world"}

@app.get("/About")              #making another endpoint
def about():
    return {"meassge":"this from about"}


# now in order to run type this in terminal
# uvicorn {fileName}:{objectName} --reload