import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "http://127.0.0.1:8080/v1/records",
            json={"title": "shoes", "descr": "new5", "owner": "big Mazzy", "status": "empty"}

        )
        print(response.status)
        print(await response.json())

        # async with session.post(
        #     'http://127.0.0.1:8080/hello/world/42?key1=val1&key2=val2',
        #     json={"some": "data"},
        #     headers={"Authorisation": "token"}
        
        # ) as response:
        #     print(response.status)
        #     print(await response.text())
        
                
        # async with session.get(
        #     'http://127.0.0.1:8080/v1/records/1'
        # ) as response:
        #     print(response.status)

                # response = await session.get("http://127.0.0.1:8080/v1/users/5")
        # print(response.status)
        # print(await response.json())


        # response = await session.delete(
        #     "http://127.0.0.1:8080/v1/records/3", json={"some": "data"}
        # )
        # print(response.status)
        #print(await response.json())

        # response = await session.post(
        #     "http://127.0.0.1:8080/v1/users",
        #     json={"name": "user_2", "password": "dfsfdgfsd"},
        # )
        # print(response.status)
        # print(await response.json())


        # response = await session.patch("http://127.0.0.1:8080/v1/users/100", json={
        #     "name": "new_name",
        # })
        # print(response.status)
        # print(await response.json())
        #
        # response = await session.get("http://127.0.0.1:8080/v1/users/1")
        # print(response.status)
        # print(await response.json())



        # response = await session.get("http://127.0.0.1:8080/v1/users/1")
        # print(response.status)
        # print(await response.json())


asyncio.run(main())
