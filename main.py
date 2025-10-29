import os
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel, select
from .models.Product import Product, ProductRequest, ProductResponse, ProductPartial

app = FastAPI()

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) #crear objecte de conexio

SQLModel.metadata.create_all(engine) #relacionar las taulas/ vincularlas

def get_db():
    db= Session(engine)
    try:
        yield db #te permite utilizar esa base de dades en las consultas posteriores, en add, get, post... etc
    finally:
        db.close()

@app.post("/product", response_model=dict, tags=["CREATE"])
def addProduct(product: ProductRequest,db:Session= Depends(get_db)):#esto es para utilizar el yiels db y llamar la base de datos #userRequest: vincula la tabla UserRequest y tiene que tener todos los atributos. lo declara con la variable user
    insert_product = Product.model_validate(product) #esto te cambie un json a sql user(json) User(sql)
    db.add(insert_product) #
    db.commit()#si no ponemos eso no funciona
    return{"msg":"afegit usuari correctament"} #devuelve a json no a diccionari

@app.get("/product/{id}", response_model=ProductResponse, tags=["READ"])
def getProduct(id:int, db:Session = Depends(get_db)):
    stmt = select(Product).where(Product.id== id) #sqlalchemy
    result = db.exec(stmt).first() #filtro para que te encuentre el primero, si no devuelve none first
    print(result) #aqui te imprime tmb le passwd pero solo en la terminal
    return ProductResponse.model_validate(result) #esto te devuelve los datos menos la contraseña

@app.get("/api/products", response_model=list[ProductResponse], tags=["READ"])
def getProducts(db:Session = Depends(get_db)):
    stmt = select(Product) #sqlalchemy
    result = db.exec(stmt).all() #filtro para que te encuentre el primero, si no devuelve none first
    print(result) #aqui te imprime tmb le passwd pero solo en la terminal
    return result #esto te devuelve los datos menos la contraseña

@app.get("/api/product_brand/{brand}", response_model=list[ProductResponse], tags=["READ"])
def getOneProduct(brand: str, db:Session = Depends(get_db)):
    stmt = select(Product).where(Product.brand == brand) #sqlalchemy
    result = db.exec(stmt).all() #filtro para que te encuentre el primero, si no devuelve none first
    print(result) #aqui te imprime tmb le passwd pero solo en la terminal
    return result #esto te devuelve los datos menos la contraseña

@app.delete("/api/product/delete/{id}", response_model=dict, tags=["DELETE"])
def deleteProduct(id: int, db:Session = Depends(get_db)):
    product = select(Product).where(Product.id == id)
    result = db.exec(product).first()# esto te cambie un json a sql user(json) User(sql)
    db.delete(result)  #
    db.commit()  # si no ponemos eso no funciona
    return {"msg": "usuari eliminat correctament"}  # devuelve a json no a diccionari

@app.get("/api/product/partial/{id}", response_model=ProductPartial, tags=["READ"])
def getProductParcial(id: int, db:Session = Depends(get_db)):
    stmt = select(Product).where(Product.id == id) #sqlalchemy
    result = db.exec(stmt).first() #filtro para que te encuentre el primero, si no devuelve none first
    print(result) #aqui te imprime tmb le passwd pero solo en la terminal
    return ProductPartial.model_validate(result)

@app.put("/api/product/update/{id}", response_model=dict[ProductRequest], tags=["READ"])
def getProductmodified(product: ProductRequest, db:Session = Depends(get_db)):
    statement = select(Product).where(product.id == id)  # esto te cambie un json a sql user(json) User(sql)
    result = db.exec(statement)
    modificar = result.one

    modificar.name = product.name
    modificar.price = product.price
    modificar.brand = product.brand
    modificar.stock = product.stock
    modificar.description = product.description

    db.add(modificar)
    db.commit()
    db.refresh(modificar)

    return{"msg":"modificat correctament"}