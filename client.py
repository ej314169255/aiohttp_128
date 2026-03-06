import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:

        # async with session.post(
        #     'http://127.0.0.1:8080/hello/world/42?key1=val1&key2=val2',
        #     json={"some": "data"},
        #     headers={"Authorisation": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.n7Uw2hjWCO0xAPKnTOohWbleRb7k0fFBfu46RrEMUseZp5JSKnudxtT0-Q3FO7YJ17suciiWxccWdxVqkCoCdw"}
        
        # ) as response:
        #     print(response.status)
        #     print(await response.text())


        # response = await session.post(
        #     "http://127.0.0.1:8080/k2/records",
        #     json={"name": "Mazzy_1", "password": "tutufor1", "token": "token_1"}

        # )
        # print(response.status)
        # print(await response.json())

        # response = await session.post(
        #     "http://127.0.0.1:8080/v1/register",
        #     json={"title": "sh", "descr": "deep woods_53", \
        #     "owner": "Big Mazzy", "status": "Mazzynio"}

        # )
        # print(response.status)
        # print(await response.json())

        # response = await session.get(
        #     "http://127.0.0.1:8080/v1/login/1",
        #     json={"name": "Big Mazzy", "password": "tutufor1", \
        #     "owner": "Big Mazzy", "status": "Mazzynio"}

        # )
        # print(response.status)
        # print(await response.json())

        async with session.post(
            'http://127.0.0.1:8080/v1/login/1', json={"password": "tutufor1"}

        ) as response:
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

        # response = await session.patch("http://127.0.0.1:8080/k2/records/5", json={
        #     "name": "python"
        # })
        # print(response.status)
        # print(await response.json())


asyncio.run(main())
