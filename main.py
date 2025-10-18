from fastapi import FastAPI

app = FastAPI()

list_users = ["Helen", "Carmen", "Cristian"]

#exercici 1. Afegir usuari
@app.post("/api/users/{id}", response_model = dict) #el {id} se pone para poder utilizar luego, no forma parte de endpoint/ruta y el response model lo tenemos que poner siempre
async def add_user(id): #aqui le pasamos por parametro el id de arriba
    list_users.append(id) #aqui añadimos un neuvo id a la lista
    dic = {} #creamos un diccionario vacio
    for i in range(len(list_users)): #bucle para recorrer cada elemento de la lista
        dic[i] = list_users[i] #crea una clave para cada elemeto de la lista
    return dic #retorna en lista

#exercici 2. Llegir- Consultar un usuari
@app.get("/api/users/{id}", response_model = dict)
async def get_user(id: int):
    dic = {}
    for i in range(len(list_users)):
        if i == id: #verificamos si el id pasado por parametro es igual que el de la lista
            dic[i] = list_users[i]
            return dic

#exercici 3. Llegir - Consultar tots els usuaris
@app.get("/api/users", response_model = dict)
async def get_users():
    dic = {}
    for i in range(len(list_users)):
        dic[i] = list_users[i]
    return dic

#exercici 4. Actualitzar - Actualització completa




#exercici 6. Eliminar - Esborrar usuari
@app.delete("/api/usuaris/{id}", response_model = dict)
async def delete_user(id: int):
    list_users.pop(id) #esto borra el id pasado por parametro
    dic = {}
    for i in range(len(list_users)):
        dic[i] = list_users[i]
    return dic