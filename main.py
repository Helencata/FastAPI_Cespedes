import os
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel, select
from .models.Product import Product, ProductRequest, ProductResponse, ProductPartial, ProductOne, ProductTwo

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
def addProduct(product: ProductRequest,db:Session= Depends(get_db)):
    insert_product = Product.model_validate(product)
    db.add(insert_product)
    db.commit()
    return{"msg":"afegit usuari correctament"} #

@app.get("/product/{id}", response_model=ProductResponse, tags=["READ ONE BY ID"])
def getProduct(id:int, db:Session = Depends(get_db)):
    stmt = select(Product).where(Product.id== id)
    result = db.exec(stmt).first()
    print(result)
    return ProductResponse.model_validate(result)

@app.get("/api/products", response_model=list[ProductResponse], tags=["READ ALL"])
def getProducts(db:Session = Depends(get_db)):
    stmt = select(Product)
    result = db.exec(stmt).all()
    print(result)
    return result

@app.get("/api/product_brand/{brand}", response_model=list[ProductResponse], tags=["READ ONE BY BRAND"])
def getOneProduct(brand: str, db:Session = Depends(get_db)):
    stmt = select(Product).where(Product.brand == brand)
    result = db.exec(stmt).all()
    print(result)
    return result

@app.delete("/api/product/delete/{id}", response_model=dict, tags=["DELETE ONE"])
def deleteProduct(id: int, db:Session = Depends(get_db)):
    product = select(Product).where(Product.id == id)
    result = db.exec(product).first()
    db.delete(result)
    db.commit()
    return {"msg": "usuari eliminat correctament"}

@app.get("/api/product/partial/{id}", response_model=ProductPartial, tags=["READ PARTIAL"])
def getProductParcial(id: int, db:Session = Depends(get_db)):
    stmt = select(Product).where(Product.id == id) #sqlalchemy
    result = db.exec(stmt).first()
    return result


@app.patch("/api/product/update/{id}", response_model=dict, tags=["UPDATE ALL"])
def update_product(id: int, product: ProductRequest, db: Session = Depends(get_db)):
    product_db = db.get(Product, id)

    product_data = product.model_dump(exclude_unset=True)
    product_db.sqlmodel_update(product_data)

    db.add(product_db)
    db.commit()
    db.refresh(product_db)

    return{"msg":"modificat correctament"}

@app.patch("/api/product/one/{id}", response_model=dict, tags=["UPDATE ONE"])
def update_one(id: int, product: ProductOne, db: Session = Depends(get_db)):
    product_db = db.get(Product, id)

    product_db.price = product.price

    db.add(product_db)
    db.commit()
    db.refresh(product_db)

    return{"msg":"camp modificat correctament"}

@app.patch("/api/product/two/{id}", response_model=dict, tags=["UPDATE TWO"])
def update_one(id: int, product: ProductTwo, db: Session = Depends(get_db)):
    product_db = db.get(Product, id)

    product_db.price = product.price
    product_db.name = product.name

    db.add(product_db)
    db.commit()
    db.refresh(product_db)

    return{"msg":"camps modificat correctament"}

