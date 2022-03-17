import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import websockets

FUA = UserAgent().chrome


async def price_game(oldprice, price, discount, site_url):
    price_list = []
    if oldprice and discount == []:
        task = [asyncio.create_task(find(obj=price[-1], to_append=price_list))]
        await asyncio.wait(task)
        fn = f"Old price: -, Discount: -%, Price: {price_list[0]}\n{site_url}"
        return fn
    elif price == []:
        return """
This game is not in the store,
It will go on sale soon
Or enter the name of the game like this: 
Elden Ring, Fallout New Vegas, Rising Storm 2 Vietnam
                """
    else:
        tasks = [
            asyncio.ensure_future(find(obj=oldprice[-1], to_append=price_list)),
            asyncio.ensure_future(find(obj=price[-1], to_append=price_list)),
            asyncio.ensure_future(find(obj=discount[-1], to_append=price_list))
        ]
        await asyncio.wait(tasks)
        fn1 = f"Old price: {price_list[0]}, Discount: {price_list[2]}%, Price: {price_list[1]}\n{site_url}"
        return fn1
        # return print(f"Old price: {price_list[0]}, Discount: {price_list[2]}%, Price: {price_list[1]}\n{site_url}")


async def find(obj, to_append):
    for i in obj:
        to_str = str(i)
        a = to_str.strip('-%')
        if a.isdigit:
            go_int = int(a)
            to_append.append(go_int)
            return go_int


async def validator(text):
    if isinstance(text, str):
        text_for_site = text.lower()
        list_split = text_for_site.split(" ")
        list_to_join = "-".join(list_split)
        list_to_str = list_to_join
        return list_to_str
    else:
        print('Name of game does exists')


class Game:

    def __init__(self, text):
        self.text = text

    async def is_valid(self):
        if isinstance(await validator(text=self.text), str):
            try:
                zaka = 'https://zaka-zaka.com/game/{}'.format(await validator(text=self.text))
                req = requests.get(zaka, headers={'User-Agent': FUA})
                code_txt = req.text
                soup = BeautifulSoup(code_txt, 'lxml')
                old_price = soup.find_all('div', class_='old-price')
                price_now = soup.find_all('div', class_='price')
                discount = soup.find_all('div', class_='discount')
                tasks = asyncio.create_task(
                    price_game(oldprice=old_price, price=price_now, discount=discount, site_url=zaka)
                )
                res = await asyncio.gather(tasks)
                return res[0]
            except IndexError:
                return """ 
                    Enter the name of the game like this:\n
                    Elden Ring, Fallout New Vegas, Rising Storm 2 Vietnam
                        """
        else:
            return print('Sorry')


# for key, value in req.request.headers.items():
#     print(key+':'+value)


async def main(text):
    gm = Game(text=text)
    return await gm.is_valid()


# async def result(text):
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(await main(text=text))
#     loop.close()
#     return result.result()

if __name__ == '__main__':
    pass
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main('Elden Ring')) # Elden Ring, Rising Storm 2 Vietnam, Fallot 3, Fallout New Vegas
    # loop.close()

"""

html = html.split('<table class="ws-table-all notranslate">')[1]

"""