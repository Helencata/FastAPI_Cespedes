from fastapi import FastAPI

app = FastAPI()

list_users = ["Helen", "Carmen", "Cristian"]

#exercici 1. Afegir usuari
@app.post("/api/users/{id}", response_model = dict) #el {id} se pone para poder utilizar luego, no forma parte de endpoint/ruta y el response model lo tenemos que poner siempre
async def add_user(id): #aqui le pasamos por parametro el id de arriba
    list_users.append(id) #aqui lo añadimos a la lista
    dic =dict(zip(list_users, range(len(list_users)))) #aqui lo transformamos en diccionario
    return dic #aqui retornamos el diccionario

#exercici 2. Llegir- Consultar un usuari
@app.get("/api/users/{id}", response_model =dict)
async def get_user(id):






@app.get("/prova/user/{user_id}")
async def read_user(user_id:int):
    return {"result": list_users[user_id-1]}

@app.post("/prova/pro")
async def prova_tres():
    return {"msg":"Hello pro"}

@app.delete("/prova/{user_id}")
async def del_user():
    return {"result": list_users}
#pueden ser mismas rutas en diferentes metodos
#el nombre de las funciones tienen que ser diferentes

#clase roger 15/10

@app.post("/hola/{id}", response_model = dict) #esto es que si o si tiene que retornar un diccionario, con eso te asegura
def addusers(id):

    #añadir nuevo usuario a list
    list.append(id)
    #convertir la lista en dict
    dict = list_users
    return dict
