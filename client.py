import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:

        # async with session.post(
        #     'http://127.0.0.1:8080/hello/world/42?key1=val1&key2=val2',
        #     json={"some": "data"},
        #     headers={"Authorisation": "token"}
        
        # ) as response:
        #     print(response.status)
        #     print(await response.text())


        response = await session.post(
            "http://127.0.0.1:8080/v1/records",
            json={"title": "shoes", "descr": "deep woods", "owner": "big Mazzy", "status": "empty"}

        )
        print(response.status)
        print(await response.json())
        
                
        # async with session.get(
        #     'http://127.0.0.1:8080/v1/records/1'

        # ) as response:
        #     print(response.status)
        #     print(await response.json())


        # response = await session.delete(
        #     "http://127.0.0.1:8080/v1/records/8", json={"some": "data"}
        # )
        # print(response.status)
        # print(await response.json())

        # response = await session.patch("http://127.0.0.1:8080/v1/records/1", json={
        #     "owner": "little mouse", "title": "snikers", "descr": "jumping"
        # })
        # print(response.status)
        # print(await response.json())


asyncio.run(main())
