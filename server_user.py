import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from db import Session, Adv, User, Token, close_orm, init_orm
from auth import hash, check

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


async def add_record(session: Session, record: User):
    try:
        session.add(record)
        await session.commit()
    except IntegrityError as err:
        raise get_error(web.HTTPConflict, {"error": "record already exists"})


class UserView(web.View):

    @property
    def record_id(self):
        return int(self.request.match_info["record_id"])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get_record(self):
        record = await self.session.get(User, self.record_id)
        if record is None:
            raise get_error(web.HTTPNotFound, "record not found")
        return record

    async def get(self):
        record = await self.get_record()
        return web.json_response(record.dict)

    async def post(self):
        json_data = await self.request.json()

        record = User(
            name=json_data["name"], password=hash(json_data["password"]),\
            token=hash(json_data["token"])
        )


        await add_record(self.session, record)
        return web.json_response(record.id_dict)

    async def patch(self):
        record = await self.get_record()
        json_data = await self.request.json()

        if "name" in json_data:
                record.name = json_data["name"]
        if "password" in json_data:
            record.password = json_data["password"]

        await add_record(self.session, record)

        return web.json_response(record.id_dict)

    async def delete(self):
        record = await self.get_record()
        record.status = "deleted"
        #await self.session.delete(record)
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
        web.post("/k2/records", UserView),
        web.get(r"/k2/records/{record_id:\d+}", UserView),
        web.patch(r"/k2/records/{record_id:\d+}", UserView),
        web.delete(r"/k2/records/{record_id:\d+}", UserView),
    ]
)

web.run_app(app)
