# field validator can only validate one field 
## but modal validator can validate more than one field at a time

from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator              #step1
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):                           #step2      creating model
    name:str   #defining schema
    email:EmailStr       #checking whether email contain @hhdfc or @icic bank is there or not  in @field validator
    age:int
    wieght:float
    married:bool = True
    allergic: Optional[List[str]]= None
    contact_details: Dict[str,str]
    
    
    
    #for verifying email is it erite or wrong
    @field_validator('email',mode="after")    #mode after take the value in field validator after data comes from patient(Basemodel) after checking
    @classmethod
    def email_validator(cls,value):           #"value" is the actual value of the email inputted by user
        
        valid_domain = ["hdfc.com","icici.com"]
        #abc@gmail.com
        domain_name = value.split("@")[-1]
        
        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        else:
            return value
        
    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator("age")
    @classmethod
    def age_valid(cls,value):
        if 0<value<100:
            return value
        raise ValueError("age should be in between 1 to 100")
    
    @model_validator(mode="after")
    def validate_emergency_contact(cls,model):
        if model.age >60 and "emergency" not in model.contact_details:
            raise ValueError("Patient older than 60 must have the emergency contacts")
        return model


def insert_patient_data(patient: Patient):             #step4
    print(patient.name)
    print(patient.age)
    print("inserted into database")

patient_info = {"name":"nitish" ,"email":"as@hdfc.com", "age" : 63, "wieght":34.4,"contact_details":{"phone":"8400434004","emergency":"328332323"}}

Patient1 = Patient(**patient_info)                     #step3    making pydantic object
insert_patient_data(Patient1)



