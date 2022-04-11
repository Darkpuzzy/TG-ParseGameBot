from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import aiohttp
from lxml import etree
from urllib.request import urlopen
import re

FUA = UserAgent().chrome
HTMLPARCE = etree.HTMLParser()
URL_ZAKA = 'https://zaka-zaka.com/game/'
URL_STEAM = 'https://store.steampowered.com/search/?term='
price_list = []


class Game:

    def __init__(self, text):
        self.text = text

    ''' PARSING STEAM STORE '''

    async def steam_find(self):
        try:
            code_txt = await client(text=await validlink(name=self.text), uri=URL_STEAM)
            with open('SteamHTML', 'w', encoding='utf-8') as f:
                f.write(code_txt)
            local = 'file:///C:/Users/user/AioAsync/SteamHTML'
            respones = urlopen(local)
            treex = etree.parse(respones, HTMLPARCE)
            task = asyncio.create_task(
                parse(uri=await linkers(
                    id=await spliter(await links(name=self.text, tree=treex), game_name=self.text),
                    list_game=await links(name=self.text, tree=treex)))
            )
            res1 = await asyncio.gather(task)
            return res1[0]
        except IndexError:
            return 'The game is not found, check if you entered the name correctly, or is missing from the store'

    ''' PARSING ZAKA-ZAKA STORE '''

    async def zaka_find(self):
        if isinstance(await validator(text=self.text), str):
            try:
                zaka = 'https://zaka-zaka.com/game/{}'.format(await validator(text=self.text))
                code_txt = await client(text=await validator(text=self.text), uri=URL_ZAKA)
                soup = BeautifulSoup(code_txt, 'lxml')
                print(soup)
                old_price = soup.find_all('div', class_='old-price')
                price_now = soup.find_all('div', class_='price')
                discount = soup.find_all('div', class_='discount')
                print(old_price)
                tasks = asyncio.create_task(price_game(oldprice=old_price, price=price_now, discount=discount, site_url=zaka))
                res2 = await asyncio.gather(tasks)
                print(res2)
                return res2[0] # В данном случае получаем фильтрованные данные
            except IndexError:
                return """
Enter the name of the game like this:\nElden Ring, Fallout New Vegas, Rising Storm 2 Vietnam 
                """
        else:
            return print('Sorry')

    async def finally_stand(self, res1, res2):
        pass


async def parse(uri):
    req_link1 = await client2(uri=uri)
    with open('SteamHTMLparse', 'w', encoding='utf-8') as f1:
        f1.write(req_link1)
    local1 = 'file:///C:/Users/user/AioAsync/SteamHTMLparse'
    respones = urlopen(local1)
    tree1 = etree.parse(respones, HTMLPARCE)
    j1 = tree1.xpath(f"//div[@class='game_area_purchase_game_wrapper']//div[@class='game_purchase_price price']")
    j2 = tree1.xpath(f"//div[@class='game_area_purchase_game_wrapper']//div[@class='discount_final_price']")
    j3 = tree1.xpath(f"//div[@class='game_area_purchase_game_wrapper']//div[@class='discount_original_price']")
    list_test = []
    if len(j3) > 0:
        for i in j2:
            priceascii = i.text
            p1 = re.search("\d[0-9]\d", str(priceascii))
            list_test.append(p1.group())
    else:
        for i in j1:
            priceascii = i.text
            p1 = re.search("\d[0-9]\d", str(priceascii))
            list_test.append(p1.group())
    final_price = await cheak_price(list_steam=list_test, list_zaka=price_list)
    if final_price == None:
        return 'Steam problems'
    else:
        return f'Price now {final_price} ₽\n{uri}'


async def cheak_price(list_steam, list_zaka):
    n = 0
    while n < len(list_steam):
        for item in list_steam:
            if item == str(list_zaka[0]):
                return item
            else:
                n+=1


async def price_game(oldprice, price, discount, site_url):
    print(oldprice)
    print(price_list)
    if oldprice and discount == []:
        future = [asyncio.ensure_future(find(obj=price[-1], to_append=price_list))]
        await asyncio.wait(future)
        return f"Old price: -, Discount: -%, Price: {price_list[0]} ₽\n{site_url}"
    elif price is []:
        return """
This game is not in the store,
It will go on sale soon
Or enter the name of the game like this: 
Elden Ring, Fallout New Vegas, Rising Storm 2 Vietnam
                """
    else:
        futures = [
            asyncio.ensure_future(find(obj=oldprice[-1], to_append=price_list)),
            asyncio.ensure_future(find(obj=price[-1], to_append=price_list)),
            asyncio.ensure_future(find(obj=discount[-1], to_append=price_list))
        ]
        await asyncio.wait(futures)
        return f"Old price: {price_list[0]} ₽, Discount: {price_list[2]}%, Price: {price_list[1]} ₽\n{site_url}"


async def links(name, tree):

    list_links = []

    for n in range(1, 20):
        j = tree.xpath(f"//div[@id='search_resultsRows']/a[{n}]")
        advacii = j[-1].attrib
        if name in advacii['href']:
            list_links.append(advacii['href'])
        elif name.capitalize() in advacii['href']:
            list_links.append(advacii['href'])
        elif name.upper() in advacii['href']:
            list_links.append(advacii['href'])

    if not list_links:
        interim_list = []
        j1 = tree.xpath(f"//div[@id='search_resultsRows']/a[1]")
        advac = j1[-1].attrib
        interim_list.append(advac['href'])
        tasks = asyncio.create_task(spliter(list_cheak=interim_list, game_name=None))
        game_name = await asyncio.gather(tasks)
        enter = game_name[0]
        return await links(name=enter, tree=tree)
    # print(list_links)
    return list_links


async def spliter(list_cheak, game_name):
    list_split = []
    n = 0
    game_n = await valid(name=game_name)
    while n < len(list_cheak):
        for i in list_cheak:
            j = i.split('/')
            list_split.extend(j)
            n += 1

    if game_n is not None:

        async def find_game_id(list_cheaker, game):
            try:
                index_game = list_cheaker.index(game)
                game_id = list_cheaker[index_game - 1]
                return game_id
            except ValueError:
                ind = 0
                while True:
                    if game.lower() == list_cheaker[ind].lower():
                        game_id = list_cheaker[ind-1]
                        break
                    else:
                        ind += 1
                        continue
                return game_id
        return await find_game_id(list_cheaker=list_split, game=game_n)
    else:
        return list_split[5]


async def linkers(id, list_game):
    for j in list_game:
        if id in j:
            return j


async def valid(name):
    if isinstance(name, str):
        text_for_site = name
        list_split = text_for_site.split(" ")
        list_to_join = "_".join(list_split)
        list_to_str = list_to_join
        return list_to_str


async def validlink(name):
    if isinstance(name, str):
        text_for_site = name
        list_split = text_for_site.split(" ")
        list_to_join = "+".join(list_split)
        list_to_str = list_to_join
        return list_to_str


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


async def client2(uri):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{uri}', headers={'User-Agent': FUA}) as response:
            html = await response.text()
            return html


async def client(text, uri):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{uri}{text}', headers={'User-Agent': FUA}) as response:
            html = await response.text()
            return html


async def main(text):
    gm = Game(text=text)
    res1 = await gm.zaka_find()
    res2 = await gm.steam_find()
    return f'Zaka-Zaka Store:\n{res1}\nSteam Store:\n{res2}\n'

# for key, value in req.request.headers.items():
#     print(key+':'+value)
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