import requests

URLethPrice = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD"
URLgodsPrice = "https://min-api.cryptocompare.com/data/price?fsym=gods&tsyms=USD"
getEthPrice = requests.get(URLethPrice)
getGodsPrice = requests.get(URLgodsPrice)

ethPrice = getEthPrice.json()['USD']
godsPrice = getGodsPrice.json()['USD']

itemsName = [  # %20
    "Celestial%20stag",
    "Faeflame%20Blade",
    "falling%20star",
    "Lightning%20Strike",
    "Marsh%20Walker",
    "sudden%20bloom",
    "Sole%20Survivor",
    "Armor%20Lurker",
    "Pyramid%20Warden",
    "Cursed%20Obelisks",
    "Another%20Round!",
    "Necroscepter",
    "Finnian%20Fruitbearer",
    "Valka's%20Captain",
    "Oddi,%20Valka’s%20Herald",
    "Defend%20the%20Ramparts",
    "Miraculous%20Familiar",
    "Moonlight%20Charm",
    "Netherswarm%20Lord",
    "The%20Hollow",
    "Radiant%20Dawn",
    "Grand%20Hall",
]

resultList = []


class ResultObj:
    name = ""
    ethVal = 0.0
    godsVal = 0.0
    diff = 0.0

    def __init__(self, name, ethVal, godsVal, diff):
        self.name = name
        self.ethVal = ethVal
        self.godsVal = godsVal
        self.diff = diff

    def ToString(self):
        print(self.name)
        print(self.ethVal)
        print(self.godsVal)
        print(self.diff)

for name in itemsName:
    URL = "https://api.x.immutable.com/v1/orders?buy_token_type=ETH&direction=asc&include_fees=true&order_by=buy_quantity&page_size=48&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&sell_token_name=" + name + "&sell_token_type=ERC721&status=active"
    page = requests.get(URL)
    jsonResp = page.json()

    URLtwo = "https://api.x.immutable.com/v1/orders?buy_token_address=0xccc8cb5229b0ac8069c51fd58367fd1e622afd97&direction=asc&include_fees=true&order_by=buy_quantity&page_size=48&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&sell_token_name=" + name + "&sell_token_type=ERC721&status=active"
    pagetwo = requests.get(URLtwo)
    jsonResptwo = pagetwo.json()

    ethVal = 0.0
    godsVal = 0.0

    for obj in jsonResp["result"]:
        decimals = obj["buy"]["data"]["decimals"]
        price = obj["buy"]["data"]["quantity"]
        priceLen = len(price)
        priceLenDif = decimals - priceLen
        if priceLenDif > 0:
            for i in range(priceLenDif):
                price = "0" + price

            price = "0." + price
        else:
            priceNumberList = list(price)
            priceNumberList.insert(abs(priceLenDif), ".")
            price = ''.join(priceNumberList)
        ethVal = float(price)*ethPrice
        break

    for obj in jsonResptwo["result"]:
        decimals = obj["buy"]["data"]["decimals"]
        price = obj["buy"]["data"]["quantity"]
        priceLen = len(price)
        priceLenDif = decimals - priceLen
        if priceLenDif > 0:
            for i in range(priceLenDif):
                price = "0" + price

            price = "0." + price
        else:
            priceNumberList = list(price)
            priceNumberList.insert(abs(priceLenDif), ".")
            price = ''.join(priceNumberList)
        godsVal = float(price)*godsPrice
        break

    diff = 0.0
    if ethVal > 0:
        diff = (godsVal / ethVal) - 1
    resultList.append(ResultObj(name, ethVal, godsVal, diff))


for obj in resultList:
    print(obj.ToString())