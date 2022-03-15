import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


FUA = UserAgent().chrome


def price_game(oldprice, price, discount, site_url):
    price_list = []
    if oldprice and discount == []:
        find(obj=price[-1], to_append=price_list)
        return f"Old price: -, Discount: -%, Price: {price_list[0]}\n{site_url}"
    elif price == []:
        return """
        This game is not in the store,\nIt will go on sale soon\nOr enter the name of the game like this : Elden Ring, Fallout New Vegas, Rising Storm 2 Vietnam
                """
    else:
        find(obj=oldprice[-1], to_append=price_list)
        find(obj=price[-1], to_append=price_list)
        find(obj=discount[-1], to_append=price_list)
        return f"Old price: {price_list[0]}, Discount: {price_list[2]}%, Price: {price_list[1]}\n{site_url}"


def find(obj, to_append):
    for i in obj:
        to_str = str(i)
        a = to_str.strip('-%')
        if a.isdigit:
            go_int = int(a)
            to_append.append(go_int)
            return go_int


def validator(text):
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

    def is_valid(self):
        if isinstance(validator(text=self.text), str):
            try:
                Zaka = 'https://zaka-zaka.com/game/{}'.format(validator(text=self.text))
                req = requests.get(Zaka, headers={'User-Agent': FUA})
                code_txt = req.text
                soup = BeautifulSoup(code_txt, 'lxml')
                old_price = soup.find_all('div', class_='old-price')
                price_now = soup.find_all('div', class_='price')
                discount = soup.find_all('div', class_='discount')
                game = price_game(oldprice=old_price, price=price_now, discount=discount, site_url=Zaka)
                return f'{game}'
            except IndexError:
                return """ 
                    Enter the name of the game like this :\nElden Ring, Fallout New Vegas, Rising Storm 2 Vietnam
                        """
        else:
            return print('Sorry')
# for key, value in req.request.headers.items():
#     print(key+':'+value)


def main(text):
    gm = Game(text=text)
    return gm.is_valid()


if __name__ == '__main__':
    pass
