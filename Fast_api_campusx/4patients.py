#Now doing the post operations




from fastapi import FastAPI, Path, HTTPException, Query   #importing FastAPI class from fastapi
                                     #Path class is used to increase the readibility of code ,by adding meta deta in functions parameter
                                     #HTTPException is import to through error 404 when data not found in db
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
import json
from fastapi.middleware.cors import CORSMiddleware


from typing import Annotated,Literal,Optional
#annotated is used to add the description
#for selcting option among given

#making object of class FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#making pydantic module
class Patient(BaseModel):
    id:Annotated[str, Field(...,description="ID of the patients",examples=["P001"])]
    name:Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="City of the Patient is living")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender:Annotated[Literal["male","female","others"],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,gt=0,description="Hieght of the patient in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Wieght of the patient in kgs")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underwieght"
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Overwieght"
        else:
            return "Obese"
        
        
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal["male","female","others"]],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]


def load_data():
    with open("1patients.json","r") as f:
        data = json.load(f)
    return data         #loading as dictionary

def save_data(data): #argument as dict
    with open("1patients.json","w") as f:
        json.dump(data,f)        #saving as json


#using decorators to make the end points - by me
@app.get("/")  #get request and  "/" is raute
def hello():
    return {"message":"Patients Management System API"}

@app.get("/About")
def About():
    return {"meassge":"A fully functional api to manage your pateints records fuck you"}

@app.get("/view")
def view():
    data = load_data()
    return data


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

    return sorted_data



@app.post("/create")
#pydatic model will automatically checks all the parameters if wrong then will throw error,#and there is no need to create object for pydantic model
def create_patient(patient:Patient): 
    
    #load exsisting data
    data = load_data()
       
    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exsists")
    
    #new patient add to the database
    
    #now storing data in dictionary gained from load_data 
    #and user inputted data is as pydantic object
    #now converting pydantic object data to dictionary
    
    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(status_code=201,content={"message":"Patient created successfully"})

    

#now updating the data
@app.put("/edit/{patient_id}")
def update_patient(patient_id:str, patient_update:PatientUpdate):
    
    #loading data
    data= load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    # so here we have excluding the only part of dict values that would be change in the nested dictioanry
    existing_patient_info = data[patient_id]
    
    
    # so patient_update data will be in pydantic object we need to convert it into dictionary
    #exclude_unset=True  is used because to remove all the information that are not inputted by the user 
    updated_patient_info = patient_update.model_dump(exclude_unset=True)


    #now changing the existing data
    for key,values in updated_patient_info.items():
        existing_patient_info[key]=values
        
    #existing_patient_info -> pydantic object -> updated bmi + verdict
    #we need to add id because in pydantic model id is there if that will not present then 
    existing_patient_info['id'] = patient_id
        
        #now unloading whole data in Patient object so can we can correct bmi and verdict
    patient_pydandic_obj = Patient(**existing_patient_info)
    
    #-> pydantic object -> dict
    #modal_dump is a pydantic function that convert pydantic object data to dictionary and exclude feature is also from pydantic
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')
    
     # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})
        
        







#now delete operation is performing
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    
    #load data
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient id doesnt exist")
    
    del data[patient_id]
    
    save_data(data)
    return JSONResponse(status_code=201,content={"message":"Patient deleted successfully"})




# now in order to run type this in terminal
# uvicorn {fileName without .py}:{objectName} --reload