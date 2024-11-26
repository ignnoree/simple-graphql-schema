from fastapi import FastAPI
import strawberry 
from strawberry.asgi import GraphQL
from typing import List
from cs50 import SQL

db=SQL('sqlite:///test.db')

@strawberry.type
class userstype:
    id:int
    author:str
    post:str



@strawberry.type
class Query:
    @strawberry.field
    def posts(self)->list[userstype]:
        posts=db.execute('select * from posts')
        return [userstype(id=row['id'], author=row['author'], post=row['post']) for row in posts]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_posts(self,author:str,post:str)->userstype:
        try:
           db.execute('INSERT INTO POSTS (author,post)VALUES(?,?)',author,post)
           createdpost1=db.execute('select * from posts where author =? and post=? order by id desc limit 1',author,post)
           createdpost=createdpost1[0]
           return userstype(id=createdpost['id'],author=createdpost['author'],post=createdpost['post'])
        except Exception as e:
            return f' error ! {str(e)}'


schema=strawberry.Schema(query=Query,mutation=Mutation)
app=FastAPI()
app.add_route("/graphql", GraphQL(schema))


@app.get('/')
def index():
    return{'homepage!'}

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host='0.0.0.0',port=8000)