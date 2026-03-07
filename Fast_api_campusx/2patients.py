from fastapi import FastAPI, Path, HTTPException, Query   #importing FastAPI class from fastapi
                                     #Path class is used to increase the readibility of code ,by adding meta deta in functions parameter
                                     #HTTPException is import to through error 404 when data not found in db

import json

#making object of class FastAPI
app = FastAPI()


#making function to load data
def load_data():
    with open("1patients.json","r") as f:
        data = json.load(f)
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



#getting particular patient data
@app.get("/patients/{patients_id}")         #{student_id} = Path parameter can be used without importing Path and this path parameter is different from path calss that is bieng imported above 
def view_patient(patients_id:str = Path(..., description="ID of the patients in the DB", example = "P001")):   
    #initial 3dots means its compulsary to provide the value , 
    #adding path class to add meta data that will be visible in fastapi docs as adocumentation
    #load all the patients
    #str = type of a variable
    data = load_data()
    
    if patients_id in data:
        return data[patients_id]
    # return {"error":"patients not found"}  #this will show error but status_code=200 \
                                              #so we need to change it to 404
    raise HTTPException(status_code=404,detail="patients not found")
                                            #in order to through 404 exception not 202 
                                            #we need to import custom Exception class HTTPException from fastapi
                                            


"""
A query parameter is data sent in the URL after ?
/sort
   ↑
endpoint

?sort_by=bmi
↑
query parameter

&order=desc
↑
another query parameter
"""


@app.get("/sort")
def sort_patients(sort_by:str = Query(...,description="sort on the basis of height, weight and bmi"),    #As you see in sort_by there is 3 dots means it compulsory
order:str = Query("asc",description="sort in asc and desc order")):                                    #but in orders "asc" is bydefault given so you can leae it    
    valid_fields= ["height","weight","bmi"]
    
    if sort_by not in valid_fields:
        raise  HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail ="Invalid order please select it between asc and desc")
    
    data = load_data()
    
    sort_order= True if order =="desc" else False
    
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)   
    # ,0 is used in for in case key is not present then it will take 0.
    
    
    #this could also have been done by x[sort_by] but in this case if value would not be found
    # then it would have through error so we use .get() function as it shows just null values when the value not found 
    
    # sorted_data = sorted(data.values(),key=lambda x:x[sort_by],reverse=sort_order)
    
    return sorted_data


# In order to use Query expresseion you must add to url = "?sort_by=bmi&order=desc"
    








# now in order to run type this in terminal
# uvicorn {fileName without .py}:{objectName} --reload