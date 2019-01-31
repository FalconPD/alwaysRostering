import AR.AR as AR
import AR.schoology as schoology
import asyncio
import logging

async def main():
    async with schoology.Session() as Schoology:
        print("Before")
        response = await Schoology.get('https://api.schoology.com/v1/users/72480022')
        user = await response.json()
        print(user)
        user['synced'] = 0
        response = await Schoology.put('https://api.schoology.com/v1/users/72480022',
            json=user)
        print("After")
        print(await response.json())

logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
