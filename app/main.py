from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)


# from

app = FastAPI()
# apps=FastAPI()

# this is the code for connecting to our database
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='1234', cursor_factory=RealDictCursor)
        # cursor_factory=RealDictCursor is used to get the column name
        # in psycopg2 module it does not provide the column name just provide the values
        # so we have to use RealDictCursor
        cursor = conn.cursor()
        print("connection Successful")
        break
    except Exception as error:
        print("connection faild")
        print("error - ", error)
        time.sleep(2)



# it is used for typechecking and maintain schema
class POST_SCHEMA(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


my_posts = [
    {
        "title": "chatgpt vs bard",
        "content": "bing is collarbating with openai",
        "id": 1
    },
    {
        "title": "rps partner",
        "content": "right path to start partner",
        "id": 2
    }]


# def fetch_post(id):
#     for p in my_posts:
#         # print(p["id"])
#         if p["id"] == id:
#             return p


# def fetch_post_index(id):
#     for i, p in enumerate(my_posts):
#         # print(p["id"])
#         if p["id"] == id:
#             return i

@app.get("/sqlalchemy")
async def test_db(db: Session = Depends(get_db)):
    return('db connection successful')


@app.get("/")
async def root():
    return {"message": "WELCOME TO MY WEBSITE"}


@app.get("/Posts")
def get_all_posts():
    cursor.execute(""" SELECT * FROM POSTS;""")
    posts = cursor.fetchall()
    return {"data": posts}
    return {"data": my_posts}


@app.get("/Posts/{id}")
# !!!!
# this is called path parameter where parameter is already provided in path or endpoint (( path parameter is always string))
def get_one_post(id: int):  # ,response:Response)
    # print(id,type(id))
    # post = fetch_post(id)
    cursor.execute("""SELECT * FROM POSTS WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with given id: {id} does not exist")

# ------------- !!! same way to do this  !!! ------------

        response.status_code = status.HTTP_404_NOT_FOUND
        return {f"Post with given id: {id} does not exist"}

    return {"post details": post}


@app.post("/Posts", status_code=status.HTTP_201_CREATED)
# this is a way of defining default status code
def create_post(post: POST_SCHEMA):
    # post_dict = post.dict()
    cursor.execute(""" INSERT INTO POSTS (title,content,publish) VALUES (%s,%s,%s) RETURNING *;""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    # ----------!!! SQL injection !!! ----------- #
    # cursor.execute(f""" INSERT INTO POSTS (title,content,publish) VALUES ('{post_dict['title']}', '{post_dict['content']}', '{post_dict['published']}') RETURNING *;""")
    # post_dict["id"] = randrange(1, 100000)
    # my_posts.append(post_dict)
    # raise HTTPException(status_code=status.HTTP_201_CREATED,detail=post_dict)
    return {"data got Inserted": new_post}

    # When we save a data, it create a pydantic model
    # pydantic model has a function called ".dict()"- which convert the pydantic into dictionary
    # print(post)  # pydantic model
    # print(post.dict())   # dictionary


@app.delete("/Posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM POSTS WHERE id = %(id)s RETURNING *;""", ({"id": id}))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    return {"message": f"post with id: {id} is deleted"}


@app.put("/Posts/{id}")
def update_post(id: int, post: POST_SCHEMA):
    QUERY = """UPDATE POSTS SET title = %(title)s, content = %(content)s, publish = %(publish)s WHERE id = %(id)s RETURNING *;"""
    payload = {"id": id, "title": post.title, "content":
               post.content, "publish": post.published}
    cursor.execute(query=QUERY, vars=payload)
    updated_post = cursor.fetchone()
    conn.commit()
    # post_index = fetch_post_index(id)

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    # upost = updated_post.dict()
    # upost["id"] = id
    # my_posts[post_index] = upost
    return {"message": updated_post}
    pass


# for debugging


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
