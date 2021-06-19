from pymongo import MongoClient

client = MongoClient()

#getting database
db = client.LOGIN

#getting document
collection = db.user_login

#insert one document
def insert_one(email,password,name='not defined'):
    user={
    "name":name,
    "email":email,
    "password":password
    }
    collection.insert_one(user)

#finding document      returns None if not present
def find_one(email):
    return collection.find_one({"email":email})

#delete 
def delete_many(email):
    collection.delete_many({"email":email})

#update history
def update(email,result):
    collection.update_one({"email":email},{"$push":{"history":result}})

# update('test@gmail.com','cough')