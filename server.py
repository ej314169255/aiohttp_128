import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from db import Session, Adv, close_orm, init_orm

app = web.Application()


async def orm_context(app: web.Application):
    print("START")
    await init_orm()
    yield
    await close_orm()
    print("FINISH")


app.cleanup_ctx.append(orm_context)


class AdvView(web.View):
    async def get(self):
        record_id = int(self.request.match_info["record_id"])
        async with Session() as session:
            record = await session.get(Adv, record_id)
            if record is None:
                raise web.HTTPNotFound(
                    text=json.dumps({"error": "record not found"}),
                    content_type="application/json",
                )
            return web.json_response(record.dict())

    async def post(self):
        json_data = await self.request.json()
        async with Session() as session:
            record = Adv(title=json_data["title"], descr=json_data["descr"],\
            owner=json_data["owner"], status=json_data["status"])
            try:
                session.add(record)
                await session.commit()
            except IntegrityError as err:
                message = {"error": "record already exists"}

                raise web.HTTPConflict(
                    text=json.dumps(message), content_type="application/json"
                )

            return web.json_response(record.dict())

    async def patch(self):
        record_id = int(self.request.match_info["record_id"])
        json_data = await self.request.json()
        async with Session() as session:
            record = await session.get(Adv, record_id)
            if record is None:
                raise web.HTTPNotFound(
                    text=json.dumps({"error": "record not found"}),
                    content_type="application/json",
                )
            if "owner" in json_data:
                record.owner = json_data["owner"]
            if "title" in json_data:
                record.title = json_data["title"]
            if "descr" in json_data:
                record.descr = json_data["descr"]
            try:
                session.add(record)
                await session.commit()
            except IntegrityError as err:
                message = {"error": "record already exists"}

                raise web.HTTPConflict(
                    text=json.dumps(message), content_type="application/json"
                )
            return web.json_response(record.dict())

    async def delete(self):
        record_id = int(self.request.match_info["record_id"])
        async with Session() as session:
            record = await session.get(Adv, record_id)
            if record is None:
                raise web.HTTPNotFound(
                    text=json.dumps({"error": "record not found"}),
                    content_type="application/json",
                )
            record.status = "deleted"
            session.add(record)
            #await session.delete(record)
            await session.commit()
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
