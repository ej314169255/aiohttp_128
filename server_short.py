import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from auth import hash_password
from db import Session, User, close_orm, init_orm

app = web.Application()


async def orm_context(app: web.Application):
    print("START")
    await init_orm()
    yield
    await close_orm()
    print("FINISH")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(error_class, message):
    return error_class(
        text=json.dumps({"error": message}), content_type="application/json"
    )


async def add_user(session: Session, user: User):
    try:
        session.add(user)
        await session.commit()
    except IntegrityError as err:
        raise get_error(web.HTTPConflict, {"error": "user already exists"})


class UserView(web.View):

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get_user(self):
        user = await self.session.get(User, self.user_id)
        if user is None:
            raise get_error(web.HTTPNotFound, "user not found")
        return user

    async def get(self):
        user = await self.get_user()
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()

        user = User(
            name=json_data["name"], password=hash_password(json_data["password"])
        )
        await add_user(self.session, user)
        return web.json_response(user.id_dict)

    async def patch(self):
        user = await self.get_user()
        user_data = await self.request.json()

        if "name" in user_data:
            user.name = user_data["name"]
        if "password" in user_data:
            user.password = hash_password(user_data["password"])
        await add_user(self.session, user)

        return web.json_response(user.id_dict)

    async def delete(self):
        user = await self.get_user()
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


async def hello_world(request: web.Request):
    json_data = await request.json()
    headers = request.headers
    qs = request.query
    some_id = int(request.match_info["some_id"])

    print(f"{json_data=}")
    print(f"{headers=}")
    print(f"{qs=}")
    print(f"{some_id=}")

    return web.json_response({"hello": "world"})


app.add_routes(
    [
        web.post(r"/hello/world/{some_id:\d+}", hello_world),
        web.post("/v1/users", UserView),
        web.get(r"/v1/users/{user_id:\d+}", UserView),
        web.patch(r"/v1/users/{user_id:\d+}", UserView),
        web.delete(r"/v1/users/{user_id:\d+}", UserView),
    ]
)

web.run_app(app)
