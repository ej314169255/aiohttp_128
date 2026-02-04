import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from auth import hash_password
from db import Session, Adv, User, close_orm, init_orm

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


async def add_record(session: Session, record: Adv):
    try:
        session.add(record)
        await session.commit()
    except IntegrityError as err:
        raise get_error(web.HTTPConflict, {"error": "record already exists"})


class AdvView(web.View):

    @property
    def record_id(self):
        return int(self.request.match_info["record_id"])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get_record(self):
        record = await self.session.get(Adv, self.record_id)
        if record is None:
            raise get_error(web.HTTPNotFound, "record not found")
        return record

    async def get(self):
        record = await self.get_record()
        return web.json_response(record.dict())

    async def post(self):
        json_data = await self.request.json()

        record = Adv(
            title=json_data["title"], descr=json_data["descr"],\
            owner=json_data["owner"], status=json_data["status"]
        )
        await add_record(self.session, record)
        return web.json_response(record.id_dict)

    async def patch(self):
        record = await self.get_record()
        json_data = await self.request.json()

        if "owner" in json_data:
                record.owner = json_data["owner"]
        if "title" in json_data:
            record.title = json_data["title"]
        if "descr" in json_data:
            record.descr = json_data["descr"]
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
        web.post("/v1/records", AdvView),
        web.get(r"/v1/records/{record_id:\d+}", AdvView),
        web.patch(r"/v1/records/{record_id:\d+}", AdvView),
        web.delete(r"/v1/records/{record_id:\d+}", AdvView),
    ]
)

web.run_app(app)
