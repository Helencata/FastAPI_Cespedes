from sqlmodel import SQLModel, Field
class Product(SQLModel, table= True): #esto conecta a la base de dades que hay en el main
    id: int  = Field(default = None, primary_key=True)
    name: str
    price: int
    brand: str
    stock: int
    description: str

class ProductRequest(SQLModel):
    name: str
    price: int
    brand: str
    stock: int
    description: str

class ProductResponse(SQLModel):
    id:int
    name: str
    price: int
    brand: str
    description: str

class ProductPartial(SQLModel):
    name: str
    price: int
    brand: str

class ProductOne(SQLModel):
    price: int

class ProductTwo(SQLModel):
    name: str
    price: int
