from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse, JSONResponse

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/html/hello', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def hello_html():
    return """
    <html>
      <head>
        <title>Hello World!</title>
      </head>
      <body>
        <h1>Hello World!</h1>
      </body>
    </html>"""


@app.get(
    '/json/hello',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
def hello_json():
    return {'message': 'Hello World!'}


@app.post(
    '/users',
    status_code=HTTPStatus.CREATED,
    response_class=JSONResponse,
    response_model=UserPublic,
    tags=['users'],
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)

    return user_with_id


@app.get(
    '/users',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserList,
    tags=['users'],
)
def get_users():
    return {'users': database}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserPublic,
    tags=['users'],
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
    tags=['users'],
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
