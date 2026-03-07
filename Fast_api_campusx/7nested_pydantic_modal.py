# using nested pydantic modal just to store data
from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str
    
class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address
    
address_dict= {"city":"Kanpur","state":"Uttar Pradesh","pin":"209206"}
address1=Address(**address_dict)

patient_dict={"name":"ayush","gender":"male","age":34,"address":address1}
patient1=Patient(**patient_dict)

print(patient1)

#extracting data as dictionary
temp=patient1.model_dump()
print(type(temp))

#extracting data as json
temp=patient1.model_dump_json
print(type(temp))

