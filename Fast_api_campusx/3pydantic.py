# from pydantic import BaseModel                      #step1

# class Patient(BaseModel):                           #step2      creating model
#     name:str                                             #defining schema
#     age:int


# def insert_patient_data(patient: Patient):             #step4
#     print(patient.name)
#     print(patient.age)
#     print("inserted into database")

# patient_info = {"name":"nitish" , "age" : 30}

# Patient1 = Patient(**patient_info)                     #step3    making pydantic object
# insert_patient_data(Patient1)





from pydantic import BaseModel,EmailStr,AnyUrl,Field                     #step1
from typing import List,Dict,Optional,Annotated


class Patient(BaseModel):                                          #step2 creating pydantic model to verify
    
    
    #By using Field and Annotated you can add meta data by providing some description
    
    name : Annotated[str,Field(max_length=50,title="Name of the Patient",description="Give the name of the patient in less than 50 words",example=["Nishit","Amit"])]                                        
    age:int
    weight: float=Field(gt=0)         #by using Field class from pydantic we restrict the field to always greater than 0
    linkdin : AnyUrl   #class that will check schema for site
    married: bool = False      #it is putting bydefault value to the married if in case not provided a
    allergies: Optional[List[str]]= None                  # Optional is the fuctionality of typing module
    contact_details: Dict[str, str]           #from pydantic module
    email : EmailStr          #will verify email correct schema

def insert_patient_data(patient: Patient):             #step4  printing all the details
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print("inserted into database")

patient_info = {"name":"nitish" , "email" : "asasus@gmail.com" , "age" : 30,"weight":68,"married":True ,
                "linkdin":"https://www.scaler.com/academy/mentee-dashboard/core-curriculum/m/70/classes","allergies":["pollen","dust"], "contact_details":{"phone":"8400434004"}}

Patient1 = Patient(**patient_info)                     #step3 making pydantic object  and unpaking dict and here process of verification will take place
insert_patient_data(Patient1)