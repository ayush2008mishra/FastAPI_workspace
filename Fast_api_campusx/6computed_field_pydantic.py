from pydantic import BaseModel,EmailStr,AnyUrl,Field,computed_field              #step1
from typing import List,Dict,Optional


class Patient(BaseModel):                           #step2      creating model
    name:str   #defining schema
    email:EmailStr       #checking whether email contain @hhdfc or @icic bank is there or not  in @field validator
    age:int
    wieght:float
    hieght:int
    married:bool = True
    allergic: Optional[List[str]]= None
    contact_details: Dict[str,str]
    
    
    #computed field is used when we want to make another field from provided input
    @computed_field
    @property
    def bmi(self) ->float:  #float will be return type
        bmi = round(self.wieght/(self.hieght**2),2)
        return bmi
    
def insert_patient_data(patient: Patient):             #step4
    print(patient.name)
    print(patient.age)
    print(patient.bmi)
    print("inserted into database")

patient_info = {"name":"nitish" ,"email":"as@hdfc.com", "age" : 63, "wieght":34.4,"hieght":34,"contact_details":{"phone":"8400434004","emergency":"328332323"}}

Patient1 = Patient(**patient_info)                     #step3    making pydantic object
insert_patient_data(Patient1)
