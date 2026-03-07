from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator                  #step1
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):                           #step2      creating model
    name:str   #defining schema
    email:EmailStr       #checking whether email contain @hhdfc or @icic bank is there or not  in @field validator
    age:int
    wieght:float
    married:bool
    allergic: List[str]
    contact_details: Dict[str,str]
    
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):           #"value" is the actual value of the email inputted by user
        
        valid_domain = ["hdfc.com","icici.com"]
        #abc@gmail.com
        domain_name = value.split("@")[-1]
        
        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        else:
            return value


def insert_patient_data(patient: Patient):             #step4
    print(patient.name)
    print(patient.age)
    print("inserted into database")

patient_info = {"name":"nitish" , "age" : 30}

Patient1 = Patient(**patient_info)                     #step3    making pydantic object
insert_patient_data(Patient1)



